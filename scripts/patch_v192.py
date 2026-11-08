#!/usr/bin/env python3
"""Patch v191 -> v192: admin bird container matches regular emoji size (17px)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v191.js'
dst = '_deploy/assets/index-DUcNPOLc-v192.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'style:{position:`relative`,display:`inline-block`,width:`14px`,height:`14px`,'
    'overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'alt:`admin`,style:{position:`absolute`,height:`22px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})]}'
)
NEW = (
    'style:{position:`relative`,display:`inline-block`,width:`17px`,height:`17px`,'
    'overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'alt:`admin`,style:{position:`absolute`,height:`26px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})]}'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: admin bird container matched to emoji size')
else:
    errors.append('FAIL: admin bird not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
