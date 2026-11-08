#!/usr/bin/env python3
"""Patch v612 -> v613: Flip the paperclip emoji horizontally using CSS transform."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v612.js'
dst = '_deploy/assets/index-DUcNPOLc-v613.js'

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
    'children:ne?`…`:`📎 Attach`})',
    'children:ne?`…`:(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`span`,{style:{display:`inline-block`,transform:`scaleX(-1)`},children:`📎`}),` Attach`]})})',
    'flip paperclip emoji'
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
