#!/usr/bin/env python3
"""Patch v1279 -> v1280: the @tag suggestion list shows each bird's own name pill (bird picture + colour, admin/mod
badges), rendered with the same Xn pill component as chirps."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1279.js'
dst = '_deploy/assets/index-DUcNPOLc-v1280.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const close=()=>{if(box){box.remove();box=null}list=[];sel=0};",
      "const close=()=>{if(box){const b=box,r=b._r;b.remove();box=null;r&&setTimeout(()=>{try{r.unmount()}catch(e){}},0)}list=[];sel=0};", 'unmount on close')
patch("const v=t.value,nv=v.slice(0,k.a)+`@`+u+` `+v.slice(k.b);close();setV(t,nv);const np=k.a+u.length+2;",
      "const v=t.value,nv=v.slice(0,k.a)+`@`+u.n+` `+v.slice(k.b);close();setV(t,nv);const np=k.a+u.n.length+2;", 'pick uses name')
patch("box.innerHTML=``;list.forEach((u,i)=>{const b=document.createElement(`button`);b.type=`button`;b.dataset.i=i;b.className=i===sel?`on`:``;b.innerHTML=`<b>@</b>`;b.appendChild(document.createTextNode(u));box.appendChild(b)});place()};",
      "if(!box._r)box._r=(0,g.createRoot)(box);box._r.render(list.map((u,i)=>(0,L.jsx)(`button`,{type:`button`,\"data-i\":i,className:i===sel?`on`:``,children:(0,L.jsx)(Xn,{record:{username:u.n,is_admin:u.r===`admin`,is_mod:u.r===`mod`,browser_id:null},name:u.n,color:u.r===`admin`?`#ffffff`:u.r===`mod`?`#c084fc`:Hn(null,u.n)})},u.n)));requestAnimationFrame(()=>requestAnimationFrame(place))};", 'render pills')
patch("list=(d.users||[]).map(x=>x.username).filter(n=>n&&n.toLowerCase()!==me).sort((a,b)=>(b.toLowerCase().startsWith(q)?1:0)-(a.toLowerCase().startsWith(q)?1:0)).slice(0,6);",
      "list=(d.users||[]).filter(x=>x.username&&x.username.toLowerCase()!==me).map(x=>({n:x.username,r:x.role})).sort((a,b)=>(b.n.toLowerCase().startsWith(q)?1:0)-(a.n.toLowerCase().startsWith(q)?1:0)).slice(0,6);", 'keep role')
patch(".pp-at button.on{background:#2a2340}.pp-at b{color:#c084fc}", ".pp-at button.on{background:#2a2340}.pp-at button{padding:7px 8px}.pp-at button>*{pointer-events:none}", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
