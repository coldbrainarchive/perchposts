#!/usr/bin/env python3
"""Patch v178 -> v179: smaller admin bird in notification panel header."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v178.js'
dst = '_deploy/assets/index-DUcNPOLc-v179.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,'
    'width:`64px`,height:`64px`,overflow:`visible`},children:['
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{'
    'position:`absolute`,height:`110px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})'
    ']})'
)
NEW = (
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,'
    'width:`44px`,height:`44px`,overflow:`visible`},children:['
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{'
    'position:`absolute`,height:`76px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})'
    ']})'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: admin bird header size reduced')
else:
    errors.append('FAIL: header bird not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
