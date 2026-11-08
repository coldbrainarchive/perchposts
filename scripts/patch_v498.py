#!/usr/bin/env python3
"""Patch v497 -> v498: Remove confirm button appears below the selected user
pill (stacked vertically, full-width) to match the invite picker style."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v497.js'
dst = '_deploy/assets/index-DUcNPOLc-v498.js'

content = open(src, encoding='utf-8').read()

# Change the container from flex-row to flex-column, and make button full-width
OLD = ('_wpRemP&&(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8,'
       'alignItems:`center`,marginBottom:8},children:[(0,L.jsx)(Xn,{record:{username:_wpRemP.u,'
       'browser_id:null,is_admin:_wpRemP.r===`admin`},name:_wpRemP.u,color:Hn(null,_wpRemP.u)}),'
       '(0,L.jsx)(`button`,{type:`button`,style:{flex:1,padding:`8px`,borderRadius:8,border:`none`,'
       'background:`#ef4444`,color:`#fff`,fontWeight:700,fontSize:12,cursor:`pointer`,'
       'touchAction:`manipulation`}')
NEW = ('_wpRemP&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:8,'
       'marginBottom:8},children:[(0,L.jsx)(Xn,{record:{username:_wpRemP.u,'
       'browser_id:null,is_admin:_wpRemP.r===`admin`},name:_wpRemP.u,color:Hn(null,_wpRemP.u)}),'
       '(0,L.jsx)(`button`,{type:`button`,style:{width:`100%`,padding:`10px`,borderRadius:10,border:`none`,'
       'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,cursor:`pointer`,'
       'touchAction:`manipulation`}')

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Remove confirm button stacked below pill')
else:
    print('FAIL'); sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
