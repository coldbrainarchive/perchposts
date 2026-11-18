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
 const[open,setOpen]=(0,_.useState)(!1),me=(0,_.useRef)(++_cuSeq),box=(0,_.useRef)(null);
 (0,_.useEffect)(()=>{if(!open)return;const out=ev=>{if(box.current&&!box.current.contains(ev.target))setOpen(!1)};const other=ev=>{if(ev.detail!==me.current)setOpen(!1)};
  document.addEventListener(`pointerdown`,out,!0);addEventListener(`pp-cu-open`,other);
  return()=>{document.removeEventListener(`pointerdown`,out,!0);removeEventListener(`pp-cu-open`,other)}},[open]);
 if(adm||!record?.username)return(0,L.jsx)(Xn,pr);
 if(open)return(0,L.jsx)(`span`,{ref:box,className:`cu-open`,children:(0,L.jsx)(Xn,pr)});
 const m={username:record.username,browser_id:record.browser_id||null,role:qn(record)?`mod`:null},k=_hxCol(m);
 return(0,L.jsx)(`button`,{ref:box,type:`button`,className:`cu-dot`,"aria-label":`Show ${name}`,title:name,style:{"--pc":k,borderColor:k,background:`color-mix(in srgb, ${k} 22%, #1b1d24)`},
  onClick:ev=>{ev.preventDefault();ev.stopPropagation();setOpen(!0);dispatchEvent(new CustomEvent(`pp-cu-open`,{detail:me.current}))},children:_hxFace(m,14)})}
'''
patch("function Xn({record:e,name:t,color:n,onClick:r}){", CU + "function Xn({record:e,name:t,color:n,onClick:r}){", 'card user component')
patch("(0,L.jsx)(Xn,{record:e,name:e.username||`Anon #${Wn(e.browser_id)}`,color:Hn(e.browser_id,e.username),onClick:e.username?t=>m(`user`,e.username,t):void 0})",
      "(0,L.jsx)(_CardUser,{record:e,name:e.username||`Anon #${Wn(e.browser_id)}`,color:Hn(e.browser_id,e.username),onClick:e.username?t=>m(`user`,e.username,t):void 0})", 'cards use it')
css = ("body .cu-dot{width:24px;height:24px;flex-shrink:0;padding:0;border-radius:999px;border:1.5px solid;display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;cursor:pointer;-webkit-tap-highlight-color:transparent;transition:transform .12s}"
       "body .cu-dot:active{transform:scale(.92)}"
       "body .cu-open{display:inline-flex}body .cu-open .user-pill{animation:cuIn .22s cubic-bezier(.3,.7,.2,1)}"
       "@keyframes cuIn{from{clip-path:inset(0 calc(100% - 24px) 0 0 round 999px)}to{clip-path:inset(0 0 0 0 round 999px)}}"
       "@media (prefers-reduced-motion: reduce){body .cu-open .user-pill{animation:none}}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
