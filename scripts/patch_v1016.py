#!/usr/bin/env python3
"""Patch v1015 -> v1016:
- New Post: the link button also shows on the huddle side (a link goes into the opening message).
- New Post: "Post" / "Start huddle" becomes a round ↑ send button like the chirp one (40px). It's grey until
  everything needed is filled in (title + body/media for a post, title + a bird for a huddle), then lights up in
  your colour. Tapping it early still says what's missing. Spinner while uploading / sending.
- Photo chirps now send like text chirps: the photo lifts out of the tray, turns your colour and glows as it flies,
  lands as a solid colour block that fades to show the photo, with the same glow ring. It no longer sits in the
  tray for up to a second waiting for the photo to download."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1015.js'
dst = '_deploy/assets/index-DUcNPOLc-v1016.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch('!_isHuddle&&(0,L.jsx)(`button`,{type:`button`,className:`np-tool`', '(0,L.jsx)(`button`,{type:`button`,className:`np-tool`', 'link on huddles too')
SPIN = '(0,L.jsx)(`svg`,{width:16,height:16,viewBox:`0 0 16 16`,fill:`none`,style:{animation:`_caSpin 0.8s linear infinite`},children:(0,L.jsx)(`circle`,{cx:8,cy:8,r:6,stroke:`currentColor`,strokeWidth:2,strokeLinecap:`round`,strokeDasharray:`28`,strokeDashoffset:`10`})})'
patch('(0,L.jsx)(`button`,{onClick:ne?void 0:ae,disabled:l||ne,className:`feed-post-action-pill`,style:{marginLeft:`auto`,background:l?`#3b1f52`:`#c084fc`,color:`#14081d`,borderColor:`#c084fc`,fontWeight:700,opacity:l?.7:1,cursor:l?`default`:`pointer`},children:ne?`Uploading…`:l?`Sending…`:_isHuddle?`Start huddle`:`Post`})',
      '(()=>{const _rd=!!a.trim()&&(_isHuddle?_hmTagged.length>0:!!(s.trim()||T))&&!ne&&!l,_lb=_isHuddle?`Start huddle`:`Post`;'
      'return(0,L.jsx)(`button`,{type:`button`,onClick:ne||l?void 0:ae,className:`np-send`+(_rd?` on`:``)+(ne||l?` busy`:``),"aria-label":ne?`Uploading…`:l?`Sending…`:_lb,title:_lb,children:ne||l?' + SPIN + ':`↑`})})()',
      'round send button')

patch('if(!a.trim())return alert(`Give your huddle a title`);', 'if(!a.trim())return alert(_isHuddle?`Give your huddle a title`:`Give your post a title`);', 'post title message')
# Photos you just uploaded show from your phone's own copy (no waiting to download them again)
patch('(0,L.jsx)(`img`,{src:n,alt:``,style:{width:`100%`,maxWidth:`100%`', '(0,L.jsx)(`img`,{src:_mtSrc(n),alt:``,style:{width:`100%`,maxWidth:`100%`', 'attachment photo local copy')
for v in ['_pAtts', '_cAtts', '_tAtts']:
    patch('src:' + v + '[0].url', 'src:_mtSrc(' + v + '[0].url)', v + ' local copy')
patch('setTimeout(()=>old.forEach(x=>x.local&&URL.revokeObjectURL(x.local)),6000)', 'setTimeout(()=>old.forEach(x=>x.local&&!x.url&&URL.revokeObjectURL(x.local)),6000)', 'keep uploaded copies')
patch('const loc=it.local;if(loc)setTimeout', 'const loc=it.local;if(loc&&!it.url)setTimeout', 'keep uploaded copies (remove)')
patch('it.url=u;it.p=1;it.xhr=null;', 'it.url=u;it.p=1;it.xhr=null;if(it.type===`image`&&it.local)(window._mtLoc||(window._mtLoc={}))[u]=it.local;', 'remember local copy')

c += r'''
function _mtSrc(u){try{return(window._mtLoc&&window._mtLoc[u])||u}catch(e){return u}}
window._mtFly=function(body,snap,done){try{
 const MQ=`img:not([src*="admin-bird"]),video`;let bub=body.querySelector(`.chat-bubble`)||body,media=bub.querySelector(MQ);const s=snap.t[0];
 const cur=()=>{if(!media||!media.isConnected){const nb=document.querySelector(`.chat-window > .chat-msg:nth-child(1 of .chat-msg--mine) .chat-bubble`);const nm=nb&&nb.querySelector(MQ);if(nm){bub=nb;media=nm}}return media};
 if(!media||!s){done();return}
 const C=window._rgbOf?window._rgbOf(body.querySelector(`.chat-msg-meta`)):`192,132,252`,G=`0 0 0 4px rgba(${C},0.6),0 0 20px rgba(${C},0.8)`,NG=`0 0 0 0px rgba(${C},0),0 0 0px rgba(${C},0)`;
 const g=document.createElement(`div`);g.className=`mt-ghost`;const gi=document.createElement(s.kind===`video`?`video`:`img`);
 if(s.kind===`video`){gi.muted=!0;gi.playsInline=!0;gi.src=s.src+`#t=0.1`}else gi.src=s.src;g.appendChild(gi);const tint=document.createElement(`div`);tint.className=`mt-tint`;g.appendChild(tint);
 const px=v=>Math.round(v)+`px`,R0=s.r;Object.assign(g.style,{left:px(R0.left),top:px(R0.top),width:px(R0.width),height:px(R0.height)});document.body.appendChild(g);
 const lift=g.animate([{transform:`scale(1)`,boxShadow:NG},{transform:`scale(1.08)`,boxShadow:G}],{duration:180,easing:`ease-out`,fill:`forwards`});
 const tl=tint.animate([{background:`rgba(${C},0)`},{background:`rgba(${C},0.3)`}],{duration:180,fill:`forwards`});
 const t0=Date.now(),ready=()=>{const m=cur();if(!m.isConnected)return!1;const r=m.getBoundingClientRect();return r.height>30&&(m.tagName===`VIDEO`||m.complete)};
 const flash=()=>{try{const bd=bub.closest(`.chat-msg-body`)||bub,br=bd.getBoundingClientRect(),o=document.createElement(`div`);o.className=`mt-flash`;
   Object.assign(o.style,{left:px(br.left),top:px(br.top),width:px(br.width),height:px(br.height),borderRadius:getComputedStyle(bd).borderTopLeftRadius||`18px`});
   document.body.appendChild(o);window._follow&&window._follow(o,bd,document.querySelector(`.chat-window`));
   o.animate([{background:`rgba(${C},1)`,boxShadow:G},{background:`rgba(${C},0.92)`,boxShadow:G,offset:.18},{background:`rgba(${C},0)`,boxShadow:G,offset:.5},{background:`rgba(${C},0)`,boxShadow:NG}],{duration:2200,easing:`ease-out`,fill:`forwards`}).onfinish=()=>o.remove()}catch(e){}};
 const fly=()=>{const m=cur();if(!m.isConnected){g.remove();done();return}const tr=m.getBoundingClientRect(),RR=getComputedStyle(m).borderRadius||`10px`,w=R0.width,h=R0.height;
  const a=g.animate([
   {left:px(R0.left),top:px(R0.top),width:px(w),height:px(h),borderRadius:`12px`,transform:`scale(1.08)`,boxShadow:G},
   {offset:.45,left:px(tr.left+tr.width/2-w/2),top:px(tr.top+tr.height/2-h/2),width:px(w),height:px(h),borderRadius:`14px`,transform:`scale(1.08)`,boxShadow:G},
   {left:px(tr.left),top:px(tr.top),width:px(tr.width),height:px(tr.height),borderRadius:RR,transform:`scale(1)`,boxShadow:G}],{duration:620,easing:`cubic-bezier(.45,0,.2,1)`,fill:`forwards`});
  try{lift.cancel();tl.cancel()}catch(e){}
  tint.animate([{background:`rgba(${C},0.3)`},{background:`rgba(${C},0.85)`,offset:.45},{background:`rgba(${C},1)`}],{duration:620,easing:`ease-in-out`,fill:`forwards`});
  let landed=!1;const land=()=>{if(landed)return;landed=!0;const m2=cur();
   const go=()=>{done();flash();g.animate([{opacity:1},{opacity:0}],{duration:140,fill:`forwards`}).onfinish=()=>g.remove()};
   if(m2&&m2.tagName===`IMG`&&!m2.complete){try{a.cancel()}catch(e){}Object.assign(g.style,{borderRadius:RR,boxShadow:G});window._follow&&window._follow(g,m2,document.querySelector(`.chat-window`));
    let f=0;const once=()=>{if(!f){f=1;go()}};m2.addEventListener(`load`,once,{once:!0});m2.addEventListener(`error`,once,{once:!0});setTimeout(once,2500)}
   else go()};
  a.onfinish=land;setTimeout(land,900)};
 const wait=()=>{if(ready()||Date.now()-t0>450)fly();else requestAnimationFrame(wait)};requestAnimationFrame(wait);
}catch(e){done()}};
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.mt-tint{position:absolute;inset:0;pointer-events:none}
.np-send{margin-left:auto;width:40px;height:40px;flex-shrink:0;border-radius:999px;border:none;padding:0;background:#2d2f3a;color:#4b5563;font-size:18px;font-weight:700;font-family:inherit;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:background .15s,color .15s;-webkit-tap-highlight-color:transparent}
.np-send.on,.np-send.busy{background:var(--me,#c084fc);color:#14081d}
.np-send.busy{cursor:default}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
