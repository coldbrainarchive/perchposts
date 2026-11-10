#!/usr/bin/env python3
"""Patch v956 -> v957: chats open where you left off.
- Your read position per chat is the newest chirp you've actually had on screen (localStorage pp_rd_<post>,
  per device). It only starts counting once the chat has settled at its opening spot, so opening a chat
  doesn't mark the bottom as read.
- First time in a chat: it opens at the oldest chirp (loads the whole chat first if needed), so you read it
  in order.
- Coming back: a "New" divider sits above the first chirp you haven't seen and the chat opens there. If
  you've seen everything it opens at the newest as before.
- While unread chirps are below you, a "↓ N new" pill (same look as the live new-chirps pill) takes you to
  the newest; it hides near the bottom and while the live pill is showing.
- Notifications, reply links, Find and taps from the post preview still go straight to their chirp."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v956.js'
dst = '_deploy/assets/index-DUcNPOLc-v957.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch('...(()=>{let _rev=[...de].reverse(),_out=[];',
      '...(()=>{const _rdS=_rdBegin(r,!_pv&&de.length>0,!!(_fid.current||a||_nc||_sy));let _rev=[...de].reverse(),_out=[];',
      'session start')
patch('_out.push(_R(_e,!!(_pv&&_e.pinned),_e.id));let _next=_rev[_i+1];',
      '_out.push(_R(_e,!!(_pv&&_e.pinned),_e.id));let _next=_rev[_i+1];'
      'if(_rdS&&_e.created_at>_rdS&&(_next?_next.created_at<=_rdS:!_hmR.current))_out.push((0,L.jsx)(`div`,{className:`rd-new`,children:(0,L.jsx)(`span`,{children:`New`})},`rdnew`));',
      'New divider')
patch('_ldO&&!_pv&&_out.push((0,L.jsx)(_Bd,{},`ldo`));return _out;',
      '_ldO&&!_pv&&_out.push((0,L.jsx)(_Bd,{},`ldo`));!_pv&&requestAnimationFrame(()=>_rdAfter(r,D.current,_hmR.current,_older));return _out;',
      'after render')
patch('"data-comment-id":_pc&&!_ps1?void 0:e.id,',
      '"data-comment-id":_pc&&!_ps1?void 0:e.id,"data-t":_pc&&!_ps1?void 0:e.created_at,', 'chirp time attr')

c += r'''
const _rd={};
function _rdGet(p){try{return localStorage.getItem(`pp_rd_`+p)}catch(e){return null}}
function _rdSet(p,t){try{const o=_rdGet(p);if(t&&(!o||t>o))localStorage.setItem(`pp_rd_`+p,t)}catch(e){}}
function _rdBegin(p,on,focus){let s=_rd[p];
 if(!on){if(s&&s.win)delete _rd[p];return s&&s.mode===`resume`?s.snap:null}
 if(s&&s.win&&!s.win.isConnected){delete _rd[p];s=null}
 if(!s){const snap=_rdGet(p);s=_rd[p]={snap,mode:focus?`focus`:snap?`resume`:`first`,state:`pos`,loads:0,readyAt:0}}
 return s.mode===`resume`?s.snap:null}
function _rdTop(w){w.scrollTop=-(w.scrollHeight)}
function _rdTo(w,el){const a=el.getBoundingClientRect(),b=w.getBoundingClientRect();w.scrollTop+=a.top-b.top-8}
function _rdMark(p,w){const s=_rd[p];if(!s||s.state!==`ready`||Date.now()<s.readyAt||document.hidden)return;
 const b=w.getBoundingClientRect();let mx=null;
 w.querySelectorAll(`.chat-msg[data-t]`).forEach(m=>{const r=m.getBoundingClientRect();if(r.bottom>b.top+4&&r.top<b.bottom-12){const t=m.dataset.t;if(!mx||t>mx)mx=t}});
 mx&&_rdSet(p,mx)}
function _rdPill(p,w){const s=_rd[p];if(!s)return;const seen=_rdGet(p);
 const n=s.state===`ready`&&seen?[...w.querySelectorAll(`.chat-msg[data-t]`)].filter(m=>m.dataset.t>seen).length:0;
 const live=[...document.querySelectorAll(`body > button`)].some(x=>x!==s.pill&&/^↓ \d+ new chirp/.test(x.textContent||``));
 const show=n>0&&Math.abs(w.scrollTop)>200&&!live&&w.isConnected;
 if(!show){if(s.pill){s.pill.remove();s.pill=null}return}
 if(!s.pill){const q=document.createElement(`button`);q.type=`button`;q.className=`rd-pill`;
  q.onclick=()=>w.scrollTo({top:0,behavior:matchMedia(`(prefers-reduced-motion: reduce)`).matches?`auto`:`smooth`});
  document.body.appendChild(q);s.pill=q}
 const r=w.getBoundingClientRect();s.pill.style.left=(r.left+r.width/2)+`px`;s.pill.style.top=(r.bottom-40)+`px`;s.pill.textContent=`↓ ${n} new`}
function _rdAfter(p,w,more,older){const s=_rd[p];if(!s||!w)return;s.win=w;
 if(!w._rdBound){w._rdBound=1;let tm=0;w.addEventListener(`scroll`,()=>{const k=w._rdPost;clearTimeout(tm);tm=setTimeout(()=>{_rdMark(k,w);_rdPill(k,w)},120)},{passive:!0});
  addEventListener(`resize`,()=>w._rdPost&&_rdPill(w._rdPost,w))}
 w._rdPost=p;
 if(s.state===`pos`){
  const settle=f=>{f();[150,500].forEach(d=>setTimeout(()=>{if(!s.moved)f()},d));s.state=`ready`;s.readyAt=Date.now()+900;
   const mv=()=>{s.moved=1;w.removeEventListener(`touchstart`,mv);w.removeEventListener(`wheel`,mv)};w.addEventListener(`touchstart`,mv,{passive:!0});w.addEventListener(`wheel`,mv,{passive:!0})};
  if(s.mode===`focus`){s.state=`ready`;s.readyAt=Date.now()+1500}
  else if(s.mode===`first`){if(more&&s.loads<1){s.loads++;older(`all=1`);return}settle(()=>_rdTop(w))}
  else{const d=w.querySelector(`.rd-new`);
   if(d)settle(()=>{const e=w.querySelector(`.rd-new`);e&&_rdTo(w,e)});
   else{const ts=[...w.querySelectorAll(`.chat-msg[data-t]`)].map(m=>m.dataset.t);
    if(!ts.some(t=>t>s.snap)){s.state=`ready`;s.readyAt=Date.now()+600}
    else if(more&&s.loads<1){s.loads++;older(`all=1`);return}
    else settle(()=>_rdTop(w))}}}
 _rdMark(p,w);_rdPill(p,w)}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.rd-new{display:flex;align-items:center;gap:8px;padding:8px 0 6px;user-select:none;flex-shrink:0}
.rd-new::before,.rd-new::after{content:"";flex:1;height:1px;background:color-mix(in srgb,var(--me,#c084fc) 55%,transparent)}
.rd-new span{font-size:11px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--me,#c084fc);padding:0 6px}
.rd-pill{position:fixed;z-index:2147482000;transform:translateX(-50%);display:inline-flex;align-items:center;height:28px;padding:0 14px;border-radius:999px;border:1px solid #c084fc;background:#c084fc;color:#14081d;font-size:12px;font-weight:800;line-height:1;font-family:inherit;cursor:pointer;box-shadow:0 0 0 3px rgba(192,132,252,.35),0 4px 16px rgba(0,0,0,.45);white-space:nowrap;animation:rdIn .22s cubic-bezier(.3,.7,.2,1)}
@keyframes rdIn{from{opacity:0;transform:translateX(-50%) translateY(8px) scale(.9)}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
