#!/usr/bin/env python3
"""Patch v1180 -> v1181 (preview): on post cards, a poster's name pill is folded into a round bird icon (ring in
their colour). Tap it: it slides open into the full name pill. Tap the open pill: what tapping a name did before.
Tapping anywhere else (or opening another) folds it back. borbie/admins, bots and news posts are unchanged;
the post page keeps the full name."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1180.js'
dst = '_deploy/assets/index-DUcNPOLc-v1181.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

CU = r'''let _cuSeq=0;
function _CardUser(pr){const{record,name,onClick}=pr,i=Jn(record),adm=record?.is_admin===!0||!!(i&&i.hat);
 const[open,setOpen]=(0,_.useState)(!1),me=(0,_.useRef)(++_cuSeq),box=(0,_.useRef)(null),w0=(0,_.useRef)(0);
 (0,_.useLayoutEffect)(()=>{if(!open||!w0.current)return;const el=box.current&&box.current.querySelector(`.user-pill`);if(!el||!el.animate)return;const w=el.getBoundingClientRect().width;if(w<=w0.current)return;try{if(matchMedia(`(prefers-reduced-motion: reduce)`).matches)return}catch(e){}el.style.overflow=`hidden`;const a=el.animate([{width:w0.current+`px`},{width:w+`px`}],{duration:300,easing:`cubic-bezier(.25,.8,.25,1)`});a.onfinish=a.oncancel=()=>{el.style.overflow=``};w0.current=0},[open]);
 (0,_.useEffect)(()=>{if(!open)return;const out=ev=>{if(box.current&&!box.current.contains(ev.target))setOpen(!1)};const other=ev=>{if(ev.detail!==me.current)setOpen(!1)};
  document.addEventListener(`pointerdown`,out,!0);addEventListener(`pp-cu-open`,other);
  return()=>{document.removeEventListener(`pointerdown`,out,!0);removeEventListener(`pp-cu-open`,other)}},[open]);
 if(adm||!record?.username)return(0,L.jsx)(Xn,pr);
 if(open)return(0,L.jsx)(`span`,{ref:box,className:`cu cu-open`,children:(0,L.jsx)(Xn,pr)});
 return(0,L.jsx)(`button`,{ref:box,type:`button`,className:`cu cu-fold`,"aria-label":`Show ${name}`,title:name,
  onClick:ev=>{ev.preventDefault();ev.stopPropagation();w0.current=ev.currentTarget.getBoundingClientRect().width;setOpen(!0);dispatchEvent(new CustomEvent(`pp-cu-open`,{detail:me.current}))},children:(0,L.jsx)(Xn,{...pr,onClick:void 0})})}
'''
patch("function Xn({record:e,name:t,color:n,onClick:r}){", CU + "function Xn({record:e,name:t,color:n,onClick:r}){", 'card user component')
patch("(0,L.jsx)(Xn,{record:e,name:e.username||`Anon #${Wn(e.browser_id)}`,color:Hn(e.browser_id,e.username),onClick:e.username?t=>m(`user`,e.username,t):void 0})",
      "(0,L.jsx)(_CardUser,{record:e,name:e.username||`Anon #${Wn(e.browser_id)}`,color:Hn(e.browser_id,e.username),onClick:e.username?t=>m(`user`,e.username,t):void 0})", 'cards use it')
css = ("body .cu{display:inline-flex;flex-shrink:0;padding:0;margin:0;border:0;background:none;font:inherit;cursor:pointer;-webkit-tap-highlight-color:transparent}"
       "body .cu-fold .user-pill{gap:0!important;padding-left:9px!important;padding-right:9px!important;transition:transform .12s}"
       "body .cu-fold:active .user-pill{transform:scale(.93)}"
       "body .cu .user-pill-name{display:inline-block;overflow:hidden;white-space:nowrap;vertical-align:bottom}"
       "body .cu-fold .user-pill-name{max-width:0;opacity:0}"
       "body .cu-open .user-pill{justify-content:flex-start}"
       "body .cu-open .user-pill-name{animation:cuFade .3s ease-out}"
       "@keyframes cuFade{from{opacity:0}to{opacity:1}}"
       "@media (prefers-reduced-motion: reduce){body .cu-open .user-pill-name{animation:none}}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
