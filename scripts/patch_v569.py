#!/usr/bin/env python3
"""Patch v568 -> v569: Remove autoPlay/loop from PostAttachment video — was crashing mobile."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v568.js'
dst = '_deploy/assets/index-DUcNPOLc-v569.js'

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
    '(0,L.jsx)(`video`,{src:n,controls:!0,autoPlay:!0,muted:!0,loop:!0,playsInline:!0,preload:`auto`,style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}})',
    '(0,L.jsx)(`video`,{src:n,controls:!0,playsInline:!0,preload:`metadata`,style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}})',
    'remove autoPlay/loop from PostAttachment video'
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
