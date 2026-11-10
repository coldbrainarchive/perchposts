#!/usr/bin/env python3
"""Patch v971 -> v972: date pill + scrubber for chats (full-screen chat on phones, chat panel on desktop).
- While you scroll a chat that's longer than ~1.5 screens, a pill at the top shows the day you're on
  (Today / Yesterday / Nov 6 / Nov 6, 2025) and a grab handle appears on the right edge. Both fade ~1.2s
  after you stop.
- Drag the handle to fly through the whole chat; the date pill rides next to it. Grabbing it loads the
  rest of the chat first if only the newest chirps are loaded.
- Read tracking: a chirp only counts as seen after ~0.5s on screen (your own chirps count at once), so
  chirps that flash past while scrubbing or flinging aren't marked read."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v971.js'
dst = '_deploy/assets/index-DUcNPOLc-v972.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch(" els.forEach(m=>{const r=m.getBoundingClientRect();if((r.bottom>b.top+4&&r.top<b.bottom-12)||m.classList.contains(`chat-msg--mine`))seen.add(m.dataset.commentId)});",
      " const vt=s.vt||(s.vt=new Map()),now=Date.now();let pend=0;"
      "els.forEach(m=>{const id=m.dataset.commentId;if(m.classList.contains(`chat-msg--mine`)){seen.add(id);return}const r=m.getBoundingClientRect();"
      "if(r.bottom>b.top+4&&r.top<b.bottom-12){if(!vt.has(id))vt.set(id,now);if(now-vt.get(id)>=500)seen.add(id);else pend=1}else vt.delete(id)});"
      "if(pend){clearTimeout(s.vtT);s.vtT=setTimeout(()=>_rdMark(p,w),540)}",
      'read needs 0.5s on screen')
patch('function _rdAfter(p,w,more,older){const s=_rd[p];if(!s||!w)return;s.win=w;s.more=more;',
      'function _rdAfter(p,w,more,older){if(w){w._sbOlder=older;w._sbMore=more}const s=_rd[p];if(!s||!w)return;s.win=w;s.more=more;',
      'expose loader to scrubber')

c += r'''
;(()=>{try{
 const RM=()=>matchMedia(`(prefers-reduced-motion: reduce)`).matches;
 const fmt=t=>{const n=new Date(),d=new Date(t);if(isNaN(d))return``;const a=new Date(n.getFullYear(),n.getMonth(),n.getDate()),b=new Date(d.getFullYear(),d.getMonth(),d.getDate()),df=Math.round((a-b)/864e5);
  if(df===0)return`Today`;if(df===1)return`Yesterday`;return d.toLocaleDateString(void 0,{month:`short`,day:`numeric`,year:d.getFullYear()!==n.getFullYear()?`numeric`:void 0})};
 const pill=document.createElement(`div`);pill.className=`sb-date`;
 const hd=document.createElement(`div`);hd.className=`sb-handle`;hd.setAttribute(`aria-hidden`,`true`);
 document.body.append(pill,hd);
 let W=null,hideT=0,drag=null;
 const ok=w=>w&&w.isConnected&&!w.closest(`.chat-preview`)&&w.getClientRects().length&&w.scrollHeight>w.clientHeight*1.5;
 const dateAt=w=>{const r=w.getBoundingClientRect(),x=r.left+r.width/2;
  for(const dy of[18,44,80,120,170]){const el=document.elementFromPoint(x,r.top+dy),m=el&&el.closest&&el.closest(`.chat-msg`);if(!m||!w.contains(m))continue;
   if(m.dataset.t)return m.dataset.t;const o=m.dataset.pinOf&&w.querySelector(`.chat-msg[data-comment-id="${CSS.escape(m.dataset.pinOf)}"]`);if(o&&o.dataset.t)return o.dataset.t}
  const all=[...w.querySelectorAll(`.chat-msg[data-t]`)];let best=null,bd=1e9;for(const m of all){const q=m.getBoundingClientRect();const d=Math.abs(q.top-r.top);if(q.bottom>r.top&&d<bd){bd=d;best=m}}return best?best.dataset.t:null};
 const place=()=>{const w=W;if(!ok(w)){pill.classList.remove(`on`);hd.classList.remove(`on`);return}
  const r=w.getBoundingClientRect(),max=w.scrollHeight-w.clientHeight,up=Math.min(max,Math.abs(w.scrollTop)),hh=44,f=max>0?up/max:0;
  const y=r.top+6+(1-f)*(r.height-hh-12);hd.style.left=(r.right-22)+`px`;hd.style.top=y+`px`;
  const t=dateAt(w);pill.textContent=t?fmt(t):``;
  if(drag){pill.style.left=(r.right-34)+`px`;pill.style.top=(y+hh/2)+`px`;pill.classList.add(`by`)}
  else{pill.style.left=(r.left+r.width/2)+`px`;pill.style.top=(r.top+10)+`px`;pill.classList.remove(`by`)}
  pill.classList.toggle(`on`,!!pill.textContent);hd.classList.add(`on`)};
 const show=w=>{W=w;place();clearTimeout(hideT);if(!drag)hideT=setTimeout(()=>{if(!drag){pill.classList.remove(`on`);hd.classList.remove(`on`)}},1200)};
 const bind=w=>{if(w._sbB)return;w._sbB=1;w.addEventListener(`scroll`,()=>{if(ok(w))requestAnimationFrame(()=>show(w))},{passive:!0})};
 setInterval(()=>{document.querySelectorAll(`.chat-window`).forEach(bind);if(W&&!ok(W)&&!drag){pill.classList.remove(`on`);hd.classList.remove(`on`)}},500);
 const toFrac=e=>{const w=W,r=w.getBoundingClientRect(),hh=44,y=Math.min(Math.max(e.clientY-drag.off,r.top+6),r.bottom-hh-6);return 1-(y-r.top-6)/(r.height-hh-12)};
 hd.addEventListener(`pointerdown`,e=>{if(!W||!ok(W))return;e.preventDefault();e.stopPropagation();const hr=hd.getBoundingClientRect();drag={off:e.clientY-hr.top,id:e.pointerId};
  try{hd.setPointerCapture(e.pointerId)}catch(x){}hd.classList.add(`drag`);clearTimeout(hideT);
  if(W._sbMore&&W._sbOlder&&!W._sbAll){W._sbAll=1;try{W._sbOlder(`all=1`)}catch(x){}}place()});
 hd.addEventListener(`pointermove`,e=>{if(!drag||!W)return;e.preventDefault();const max=W.scrollHeight-W.clientHeight;W.scrollTop=-(toFrac(e)*max);place()});
 const end=e=>{if(!drag)return;drag=null;hd.classList.remove(`drag`);try{hd.releasePointerCapture(e.pointerId)}catch(x){}if(W)show(W)};
 hd.addEventListener(`pointerup`,end);hd.addEventListener(`pointercancel`,end);
 addEventListener(`resize`,()=>W&&place());
 const s=document.createElement(`style`);s.textContent=`
.sb-date{position:fixed;z-index:60;transform:translate(-50%,0);height:24px;line-height:24px;padding:0 11px;border-radius:999px;background:rgba(27,29,36,.92);border:1px solid rgba(148,163,184,.22);color:#e2e8f0;font-size:12px;font-weight:700;white-space:nowrap;pointer-events:none;opacity:0;transition:opacity .2s;box-shadow:0 4px 14px rgba(0,0,0,.35);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
.sb-date.on{opacity:1}
.sb-date.by{transform:translate(-100%,-50%);height:28px;line-height:28px;font-size:13px;padding:0 13px;border-color:#c084fc;transition:opacity .2s}
.sb-handle{position:fixed;z-index:61;width:16px;height:44px;border-radius:999px;background:rgba(148,163,184,.45);border:1px solid rgba(255,255,255,.12);opacity:0;pointer-events:none;transition:opacity .2s,background .15s,width .15s;touch-action:none;cursor:grab;box-sizing:border-box}
.sb-handle::after{content:"";position:absolute;inset:-14px -12px;}
.sb-handle.on{opacity:1;pointer-events:auto}
.sb-handle.drag{background:#c084fc;cursor:grabbing}
@media (hover:hover){.sb-handle.on:hover{background:rgba(192,132,252,.8)}}
@media (prefers-reduced-motion: reduce){.sb-date,.sb-handle{transition:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
