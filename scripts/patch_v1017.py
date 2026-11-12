#!/usr/bin/env python3
"""Patch v1016 -> v1017: photo chirps send as smoothly as text chirps.
Before: the tray vanished at once (chat dropped ~110px), the full-height photo chirp appeared at once (older chirps
jumped up ~310px), and the photo dashed across the screen at tile size and then grew.
Now:
- The tray shrinks away smoothly instead of vanishing.
- The new chirp's space opens up gradually, so older chirps slide up.
- The photo makes one smooth glide-and-grow into that space with the same easing and timing as a text chirp,
  following the space as it opens (it can't overshoot or land somewhere the chirp isn't any more),
  turning your colour and glowing on the way, then the same flash as text when it lands."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1016.js'
dst = '_deploy/assets/index-DUcNPOLc-v1017.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("const _ms=window._mtSnapTake&&window._mtSnapTake();",
      "const _ms=window._mtSnapTake&&window._mtSnapTake();if(_ms){H.classList.add('mt-sending');setTimeout(()=>H.classList.remove('mt-sending'),2500)}", 'hold the new chirp closed')
patch("{window._mtFly(body,_ms,done);return}const bub=body&&(",
      "{window._mtFly(body,_ms,done);return}H.classList.remove('mt-sending');const bub=body&&(", 'release if not a photo')
patch('if(!it.length)return null;',
      'if(!it.length)return S.closeH?(0,L.jsx)(`div`,{className:`mt-collapse`,style:{"--h":S.closeH+`px`},onAnimationEnd:()=>{S.closeH=0;force()}}):null;', 'tray shrinks away')
patch('function _mtPick(S,files,setCA,setUL){S.setCA=setCA;S.setUL=setUL;', 'function _mtPick(S,files,setCA,setUL){S.setCA=setCA;S.setUL=setUL;S.closeH=0;', 'new pick cancels shrink')

c += r'''
;(()=>{const old=window._mtSnapTake;window._mtSnapTake=function(){const r=old&&old();if(r){const w=document.querySelector(`.chat-compose .mt-wrap`);_mtChat.closeH=w?w.offsetHeight:0}return r}})();
function _mtBz(x1,y1,x2,y2){return t=>{if(t<=0)return 0;if(t>=1)return 1;let a=0,b=1,u=t;for(let i=0;i<24;i++){u=(a+b)/2;const x=3*(1-u)*(1-u)*u*x1+3*(1-u)*u*u*x2+u*u*u;if(x<t)a=u;else b=u}return 3*(1-u)*(1-u)*u*y1+3*(1-u)*u*u*y2+u*u*u}}
window._mtFly=function(body,snap,done){const H=document.documentElement;let rowS=null;
 const release=()=>{H.classList.remove(`mt-sending`);if(rowS){rowS.style.height=``;rowS.style.overflow=``;rowS.style.flexShrink=``;rowS.style.marginTop=``}};
 try{
 const MQ=`img:not([src*="admin-bird"]),video`,NEW=`.chat-window > .chat-msg:nth-child(1 of .chat-msg--mine)`;
 let bub=body.querySelector(`.chat-bubble`)||body,media=bub.querySelector(MQ);const s=snap.t[0];
 const cur=()=>{if(!media||!media.isConnected){const nb=document.querySelector(NEW+` .chat-bubble`);const nm=nb&&nb.querySelector(MQ);if(nm){bub=nb;media=nm}}return media};
 const row=()=>{const m=cur();return m&&m.closest(`.chat-msg`)};
 if(!media||!s||matchMedia(`(prefers-reduced-motion: reduce)`).matches){release();done();return}
 const C=window._rgbOf?window._rgbOf(body.querySelector(`.chat-msg-meta`)):`192,132,252`,G=`0 0 0 4px rgba(${C},0.6),0 0 20px rgba(${C},0.8)`,NG=`0 0 0 0px rgba(${C},0),0 0 0px rgba(${C},0)`;
 const g=document.createElement(`div`);g.className=`mt-ghost`;const gi=document.createElement(s.kind===`video`?`video`:`img`);
 if(s.kind===`video`){gi.muted=!0;gi.playsInline=!0;gi.src=s.src+`#t=0.1`}else gi.src=s.src;g.appendChild(gi);const tint=document.createElement(`div`);tint.className=`mt-tint`;g.appendChild(tint);
 const px=v=>Math.round(v)+`px`,R0=s.r;Object.assign(g.style,{left:px(R0.left),top:px(R0.top),width:px(R0.width),height:px(R0.height),boxShadow:G});tint.style.background=`rgba(${C},0.3)`;document.body.appendChild(g);
 const flash=()=>{try{const bd=bub.closest(`.chat-msg-body`)||bub,br=bd.getBoundingClientRect(),o=document.createElement(`div`);o.className=`mt-flash`;
   Object.assign(o.style,{left:px(br.left),top:px(br.top),width:px(br.width),height:px(br.height),borderRadius:getComputedStyle(bd).borderTopLeftRadius||`18px`});
   document.body.appendChild(o);window._follow&&window._follow(o,bd,document.querySelector(`.chat-window`));
   o.animate([{background:`rgba(${C},1)`,boxShadow:G},{background:`rgba(${C},0.92)`,boxShadow:G,offset:.18},{background:`rgba(${C},0)`,boxShadow:G,offset:.5},{background:`rgba(${C},0)`,boxShadow:NG}],{duration:2200,easing:`ease-out`,fill:`forwards`}).onfinish=()=>o.remove()}catch(e){}};
 const E=_mtBz(.3,.7,.2,1),DUR=720,GAP=460,t0=Date.now(),CW=document.querySelector(`.chat-window`),stick=!!CW&&Math.abs(CW.scrollTop)<=60;let full=0,start=0,landed=!1,gapPx=null;
 const ready=()=>{const m=cur();return m&&m.isConnected&&(m.tagName===`VIDEO`||m.complete)};
 const measure=()=>{const r=row();if(!r)return 0;r.style.overflow=`hidden`;return r.scrollHeight};
 const land=()=>{if(landed)return;landed=!0;release();
  const go=()=>{done();flash();g.animate([{opacity:1},{opacity:0}],{duration:140,fill:`forwards`}).onfinish=()=>g.remove()};
  const m=cur();if(m&&m.tagName===`IMG`&&!m.complete){window._follow&&window._follow(g,m,document.querySelector(`.chat-window`));let f=0;const once=()=>{if(!f){f=1;go()}};m.addEventListener(`load`,once,{once:!0});m.addEventListener(`error`,once,{once:!0});setTimeout(once,2500)}else go()};
 const frame=()=>{if(landed)return;const now=Date.now();
  if(!start){if(ready()||now-t0>450){start=now;full=measure()}else{requestAnimationFrame(frame);return}}
  const tg=Math.min(1,(now-start)/GAP),tf=Math.min(1,(now-start)/DUR),k=E(tf);
  if(stick&&CW.isConnected&&CW.scrollTop!==0)CW.scrollTop=0;const r=row();if(r){if(r!==rowS){if(rowS){rowS.style.height=``;rowS.style.overflow=``;rowS.style.flexShrink=``;rowS.style.marginTop=``}rowS=r;if(!full)full=measure()}r.style.overflow=`hidden`;r.style.flexShrink=`0`;r.style.height=tg<1?px(full*E(tg)):`auto`;if(gapPx===null){const cs=getComputedStyle(r);gapPx=(parseFloat(getComputedStyle(r.parentElement).rowGap)||0)+(parseFloat(cs.marginTop)||0)+(parseFloat(cs.marginBottom)||0)}r.style.marginTop=tg<1&&gapPx?px((parseFloat(getComputedStyle(r).marginTop)||0)*0-gapPx*(1-E(tg))):`0px`}
  const m=cur();if(!m||!m.isConnected){g.remove();release();done();return}
  const tr=m.getBoundingClientRect(),L=(a,b)=>a+(b-a)*k;
  Object.assign(g.style,{left:px(L(R0.left,tr.left)),top:px(L(R0.top,tr.top)),width:px(L(R0.width,tr.width)),height:px(L(R0.height,tr.height)),borderRadius:px(L(12,parseFloat(getComputedStyle(m).borderRadius)||10))});
  tint.style.background=`rgba(${C},${Math.min(1,.3+.7*Math.min(1,tf/.45))})`;
  if(tf>=1&&tg>=1){land();return}requestAnimationFrame(frame)};
 requestAnimationFrame(frame);setTimeout(()=>{if(!landed){landed=!0;release();g.remove();done()}},4000);
}catch(e){release();done()}};
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.mt-sending .chat-window > .chat-msg:nth-child(1 of .chat-msg--mine){height:0;overflow:hidden;flex-shrink:0;margin-top:-14px}
.mt-collapse{height:0;animation:mtCollapse .34s cubic-bezier(.3,.7,.2,1) .09s both}
@keyframes mtCollapse{from{height:var(--h)}to{height:0}}
@media (prefers-reduced-motion: reduce){.mt-collapse{animation:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
