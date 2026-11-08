#!/usr/bin/env python3
"""Patch v571 -> v574: Remove poster ghosting — strip poster attribute on play."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v571.js'
dst = '_deploy/assets/index-DUcNPOLc-v574.js'

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
    'controls:!0,playsInline:!0,preload:`metadata`,...(_vpost?{poster:_vpost}:{}),style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}',
    'controls:!0,playsInline:!0,preload:`metadata`,...(_vpost?{poster:_vpost}:{}),onPlay:_vpe=>{_vpe.target.removeAttribute(`poster`)},style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}',
    'strip poster on play to remove ghosting'
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
