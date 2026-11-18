#!/usr/bin/env python3
"""Patch v1170 -> v1171: Members sheet tidy-up.
- Leave / Delete move off the header into your own row's ⋯ menu ("Leave huddle", and "Delete huddle" for the owner).
  The "You" tag goes; the header only has + Invite.
- The sheet's colour runs down behind Safari's bottom bar."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1170.js'
dst = '_deploy/assets/index-DUcNPOLc-v1171.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("children:[me===(post.username||``).toLowerCase()&&!post.locked&&act.del?(0,L.jsx)(`button`,{type:`button`,className:`hx-addb hx-lvb hx-delb`,onClick:()=>{close();setTimeout(()=>act.del(),230)},children:`Delete`}):null,(0,L.jsx)(`button`,{type:`button`,className:`hx-addb hx-lvb`,onClick:()=>{close();setTimeout(()=>act.leave(),230)},children:`Leave`}),",
      "children:[", 'header: invite only')
patch("const more=(m,ev)=>{",
      "const mine=(ev)=>{ev.stopPropagation();const own=me===(post.username||``).toLowerCase()&&!post.locked&&act.del;_prFilterMenu(ev.currentTarget,null,[[`leave`,null,`Leave huddle`],...(own?[[`del`,null,`Delete huddle`]]:[])],k=>{close();setTimeout(()=>k===`del`?act.del():act.leave(),230)});const mm=document.querySelector(`.cp-menu`);if(mm)mm.classList.add(`hx-menu`)};\n const more=(m,ev)=>{",
      'own-row menu')
patch("m.username.toLowerCase()===me?(0,L.jsx)(`span`,{className:`hx-tag`,children:`You`},`y`):null,",
      "m.username.toLowerCase()===me?(act&&amIn?(0,L.jsx)(`button`,{type:`button`,className:`hx-more`,\"aria-label\":`Your options`,onClick:mine,children:`⋯`},`me`):(0,L.jsx)(`span`,{className:`hx-tag`,children:`You`},`y`)):null,",
      'your row gets ⋯')
patch("body .lb-ic{",
      "body .hx-sheet{box-shadow:0 -8px 40px rgba(0,0,0,.4),0 400px 0 0 #161920}"
      "body .hx-menu .cp-opt[data-k=leave],body .hx-menu .cp-opt[data-k=del]{color:#f87171}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
