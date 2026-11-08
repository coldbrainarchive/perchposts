#!/usr/bin/env python3
"""Patch v215 -> v216: Random → accent purple; Questions emoji → ❔."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v215.js'
dst = '_deploy/assets/index-DUcNPOLc-v216.js'

content = open(src, encoding='utf-8').read()
errors = []

# Random colour → accent purple
OLD_COLOR = 'random:`#a78bfa`'
NEW_COLOR = 'random:`#c084fc`'
if OLD_COLOR in content:
    content = content.replace(OLD_COLOR, NEW_COLOR, 1)
    print('OK: Random → accent purple')
else:
    errors.append('FAIL: random colour not found')

# Questions emoji → ❔
OLD_ICON = '{name:`Questions`,slug:`feedback`,icon:`💬`}'
NEW_ICON = '{name:`Questions`,slug:`feedback`,icon:`❔`}'
if OLD_ICON in content:
    content = content.replace(OLD_ICON, NEW_ICON)
    print('OK: Questions emoji → ❔')
else:
    errors.append('FAIL: Questions board not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
