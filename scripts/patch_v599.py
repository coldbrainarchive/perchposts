#!/usr/bin/env python3
"""Patch v597 -> v599: Fix scroll-to-bottom on post/huddle open.
Keep oldest-first sort. Add a delayed re-scroll (400ms) after initial comment load
so images have time to establish their height before the final scroll fires."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v597.js'
dst = '_deploy/assets/index-DUcNPOLc-v599.js'

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

# Scroll immediately AND schedule a delayed re-scroll so images don't throw off position
patch(
    'let e=D.current;e&&O.current&&(e.scrollTop=e.scrollHeight)},[u.length,g.length])',
    'let e=D.current;if(!e)return;e.scrollTop=e.scrollHeight;setTimeout(()=>{const _e=D.current;_e&&(_e.scrollTop=_e.scrollHeight)},400)},[u.length,g.length])',
    'scroll to bottom immediately + delayed re-scroll for image loads'
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
