#!/usr/bin/env python3
"""Patch v502 -> v503: Remove 📌 emoji from pin action buttons."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v502.js'
dst = '_deploy/assets/index-DUcNPOLc-v503.js'

content = open(src, encoding='utf-8').read()
errors = []

replacements = [
    ('`📌 Pin`',        '`Pin`'),
    ('`📌 Unpin`',      '`Unpin`'),
    ('`📌 Pin to Board`', '`Pin to Board`'),
    ('`📌 Pin to Forum`', '`Pin to Forum`'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f'OK: {old} -> {new}')
    else:
        errors.append(f'FAIL: {old} not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
