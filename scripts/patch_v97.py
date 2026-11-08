#!/usr/bin/env python3
"""Patch v96 -> v97: make signup pill use user-pill class, matching everywhere else."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v96.js'
dst = '_deploy/assets/index-DUcNPOLc-v97.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_PILL = (
    "style:{display:`inline-flex`,alignItems:`center`,gap:6,padding:`6px 14px 6px 10px`,"
    "borderRadius:999,"
    "border:_gu?`1.5px solid ${Hn(null,_gu)}`:`1.5px dashed #3f4756`,"
    "background:_gu?Hn(null,_gu).replace('hsl(','hsla(').replace(')',', 0.12)'):`transparent`,"
    "color:_gu?Hn(null,_gu):`#64748b`,"
    "fontSize:13,fontWeight:700,lineHeight:1,whiteSpace:`nowrap`,cursor:`pointer`,"
    "userSelect:`none`,flexShrink:0,boxSizing:`border-box`},"
    "children:[(0,L.jsx)(`span`,{style:{fontSize:15},children:`\U0001f424`}),"
    "(0,L.jsx)(`span`,{children:_gu||`tap to generate username`})]}"
)

NEW_PILL = (
    "className:`user-pill`,"
    "style:{"
    "color:_gu?Hn(null,_gu):`#64748b`,"
    "background:_gu?`${Hn(null,_gu)}18`:`transparent`,"
    "borderColor:_gu?`${Hn(null,_gu)}55`:`#3f4756`,"
    "borderStyle:_gu?`solid`:`dashed`,"
    "cursor:`pointer`,userSelect:`none`"
    "},"
    "children:["
    "(0,L.jsx)(`span`,{className:`user-pill-badge`,children:`\U0001f424`}),"
    "(0,L.jsx)(`span`,{className:`user-pill-name`,style:{maxWidth:`none`},children:_gu||`tap to generate username`})"
    "]}"
)

if OLD_PILL in content:
    content = content.replace(OLD_PILL, NEW_PILL, 1)
    print('OK: signup pill now uses user-pill class')
else:
    errors.append('FAIL: old pill pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
