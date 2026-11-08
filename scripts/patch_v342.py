#!/usr/bin/env python3
"""Patch v341 -> v342: remove up/down arrow buttons next to sort toggle."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v341.js'
dst = '_deploy/assets/index-DUcNPOLc-v342.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>{window.scrollTo({top:0,behavior:`smooth`}),document.documentElement.scrollTo({top:0,behavior:`smooth`})},style:{display:`inline-flex`,alignItems:`center`,justifyContent:`center`,width:26,height:26,borderRadius:999,border:`none`,background:`#20262f`,color:`#dbe4ee`,fontSize:12,fontWeight:800,cursor:`pointer`,flexShrink:0},children:`↑`}),'
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>{window.scrollTo({top:document.body.scrollHeight,behavior:`smooth`}),document.documentElement.scrollTo({top:document.documentElement.scrollHeight,behavior:`smooth`})},style:{display:`inline-flex`,alignItems:`center`,justifyContent:`center`,width:26,height:26,borderRadius:999,border:`none`,background:`#20262f`,color:`#dbe4ee`,fontSize:12,fontWeight:800,cursor:`pointer`,flexShrink:0},children:`↓`}),'
)
if OLD in content:
    content = content.replace(OLD, '', 1)
    print('OK: up/down arrow buttons removed')
else:
    errors.append('FAIL: arrow buttons not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
