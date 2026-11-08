#!/usr/bin/env python3
"""Patch v364 -> v365: remove back arrow from new post page nav row."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v364.js'
dst = '_deploy/assets/index-DUcNPOLc-v365.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>r(-1),style:{display:`inline-flex`,'
    'alignItems:`center`,justifyContent:`center`,width:22,height:22,borderRadius:999,'
    'border:`1px solid #323b48`,background:`#1d242d`,color:`#dbe4ee`,fontSize:11,'
    'fontWeight:800,cursor:`pointer`,flexShrink:0,boxSizing:`border-box`},'
    'children:`←`}),'
)
if OLD in content:
    content = content.replace(OLD, '', 1)
    print('OK: back arrow removed')
else:
    errors.append('FAIL: back arrow not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
