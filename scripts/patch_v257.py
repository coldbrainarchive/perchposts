#!/usr/bin/env python3
"""Patch v256 -> v257: remove emojis from USER, RANK, HATCH DATE, WORM COUNT labels."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v256.js'
dst = '_deploy/assets/index-DUcNPOLc-v257.js'

content = open(src, encoding='utf-8').read()
errors = []

replacements = [
    ('children:`\U0001f426 User`',   'children:`USER`'),
    ('children:`\U0001f947 Rank`',   'children:`RANK`'),
    ('children:`\U0001f95a Hatch Date`', 'children:`HATCH DATE`'),
    ('children:`\U0001fab1 Worm Count`', 'children:`WORM COUNT`'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f'OK: {old[:30]}… → {new[:30]}…')
    else:
        errors.append(f'FAIL: {old[:40]} not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
