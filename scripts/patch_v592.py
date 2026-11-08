#!/usr/bin/env python3
"""Patch v591 -> v592: Tap username area opens action menu."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v591.js'
dst = '_deploy/assets/index-DUcNPOLc-v592.js'

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
    'className:`chat-msg-meta`,style:{background:e.is_admin===true?`#ffffff`:h}',
    'className:`chat-msg-meta`,onClick:()=>!p&&y(_s=>!_s),style:{cursor:`pointer`,background:e.is_admin===true?`#ffffff`:h}',
    'tap username opens action menu'
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
