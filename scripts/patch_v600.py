#!/usr/bin/env python3
"""Patch v599 -> v600: Make pinned comment styling more visible with accent color."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v599.js'
dst = '_deploy/assets/index-DUcNPOLc-v600.js'

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

# Increase pinned bubble background opacity and add a visible left border
patch(
    'style:e.pinned?{background:`rgba(192,132,252,0.06)`}:void 0',
    'style:e.pinned?{background:`rgba(192,132,252,0.12)`,borderLeft:`3px solid #c084fc`,paddingLeft:8}:void 0',
    'pinned comment accent color more visible'
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
