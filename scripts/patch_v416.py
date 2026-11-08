#!/usr/bin/env python3
"""Patch v415 -> v416: add className to PTR strip so desktop can hide it via CSS"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v415.js'
dst = '_deploy/assets/index-DUcNPOLc-v416.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '(0,L.jsx)(`div`,{style:{position:`fixed`,top:0,left:0,right:0,height:`calc(${y?60:g*60}px + env(safe-area-inset-top))`'
NEW = '(0,L.jsx)(`div`,{className:`ptr-strip`,style:{position:`fixed`,top:0,left:0,right:0,height:`calc(${y?60:g*60}px + env(safe-area-inset-top))`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: ptr-strip className added')
else:
    errors.append('FAIL: spinner container not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
