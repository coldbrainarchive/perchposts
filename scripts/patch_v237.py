#!/usr/bin/env python3
"""Patch v236 -> v237: remove Utilities card from mod panel."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v236.js'
dst = '_deploy/assets/index-DUcNPOLc-v237.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '`div`,{style:{display:`grid`,gridTemplateColumns:`repeat(auto-fit, minmax(280px, 1fr))`,gap:16,marginBottom:24},'
    'children:(0,L.jsxs)(`div`,{className:`content-card`,style:{display:`flex`,flexDirection:`column`,gap:12},'
    'children:[(0,L.jsx)(`h3`,{style:{margin:0,color:`#f8fafc`,fontSize:16,fontWeight:700},children:`Utilities`}),'
    '(0,L.jsx)(`button`,{onClick:ve,style:{padding:`10px 16px`,borderRadius:12,border:`1px solid #374151`,'
    'background:`#1f2937`,color:`#f8fafc`,fontWeight:700,cursor:`pointer`,fontSize:14},children:`\U0001f6aa Leave`}),'
    '(0,L.jsxs)(`div`,{style:{display:`grid`,gap:8},children:[(0,L.jsx)(`input`,{type:`password`,'
    'placeholder:`New password`,value:de,onChange:e=>fe(e.target.value),style:{width:`100%`,'
    'boxSizing:`border-box`,padding:`11px 14px`,borderRadius:10,border:`1px solid #3f4756`,'
    'fontSize:16,background:`#0f1117`,color:`#f8fafc`}}),(0,L.jsx)(`button`,{onClick:ye,'
    'style:{width:`100%`,padding:`10px 16px`,borderRadius:12,border:`none`,background:`#c084fc`,'
    'color:`#14081d`,fontWeight:700,cursor:`pointer`,fontSize:14},children:`Update Password`})]})]})})'
)
NEW = '`div`,{style:{display:`grid`,gridTemplateColumns:`repeat(auto-fit, minmax(280px, 1fr))`,gap:16,marginBottom:24},children:null}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Utilities card removed')
else:
    errors.append('FAIL: Utilities card not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
