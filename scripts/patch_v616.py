#!/usr/bin/env python3
"""Patch v615 -> v616:
Make the attachment preview pop-in animation more dramatic and noticeable.
Scales from 0.75 -> 1.05 -> 1.0 (bounce), fades in, 0.35s duration.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v615.js'
dst = '_deploy/assets/index-DUcNPOLc-v616.js'

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

# More dramatic bounce keyframe
patch(
    '@keyframes _ppIn{from{opacity:0;transform:scale(0.92)}to{opacity:1;transform:scale(1)}}',
    '@keyframes _ppIn{0%{opacity:0;transform:scale(0.75)}80%{opacity:1;transform:scale(1.04)}100%{opacity:1;transform:scale(1)}}',
    'more dramatic _ppIn bounce keyframe'
)

# Longer duration
patch(
    'animation:`_ppIn 0.25s ease-out`',
    'animation:`_ppIn 0.35s ease-out`',
    'increase animation duration'
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
