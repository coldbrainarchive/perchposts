#!/usr/bin/env python3
"""Patch v286 -> v287: Make Xn hat bird image match inline pill style —
small contained 16x16 block image instead of large absolutely-positioned floating bird."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v286.js'
dst = '_deploy/assets/index-DUcNPOLc-v287.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_HAT_BIRD = (
    'typeof i===`object`&&i.hat?'
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,'
    'style:{position:`absolute`,height:`1.85em`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`,pointerEvents:`none`}})'
)
NEW_HAT_BIRD = (
    'typeof i===`object`&&i.hat?'
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,'
    'style:{height:16,width:16,objectFit:`contain`,display:`block`,flexShrink:0,pointerEvents:`none`}})'
)

if OLD_HAT_BIRD in content:
    content = content.replace(OLD_HAT_BIRD, NEW_HAT_BIRD, 1)
    print('OK: Xn hat bird uses small contained 16x16 image')
else:
    errors.append('FAIL: hat bird absolute style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
