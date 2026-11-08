#!/usr/bin/env python3
"""Patch v577 -> v578: Remove expand icon from images."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v577.js'
dst = '_deploy/assets/index-DUcNPOLc-v578.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append(f'FAIL ({label}): not found')
    elif n > 1:
        errors.append(f'FAIL ({label}): {n} matches (not unique)')
    else:
        content = content.replace(old, new)
        print(f'OK: {label}')

patch(
    ',(0,L.jsx)(`div`,{style:{position:`absolute`,bottom:8,right:8,background:`rgba(0,0,0,0.45)`,backdropFilter:`blur(4px)`,borderRadius:8,padding:`4px 8px`,fontSize:18,color:`#fff`,pointerEvents:`none`,lineHeight:1},children:`⤢`})',
    '',
    'remove expand icon from images'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print(f'Paren delta: {p_delta}, Brace delta: {b_delta}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
