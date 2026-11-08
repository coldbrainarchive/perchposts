#!/usr/bin/env python3
"""Patch v202 -> v203: rename Activity board to Flock with 🪶 icon (slug unchanged)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v202.js'
dst = '_deploy/assets/index-DUcNPOLc-v203.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '{name:`Activity`,slug:`activity`,icon:`⚡`,virtual:!0}'
NEW = '{name:`Flock`,slug:`activity`,icon:`🪶`,virtual:!0}'

if OLD in content:
    content = content.replace(OLD, NEW)
    print('OK: Activity board → Flock with 🪶')
else:
    errors.append('FAIL: Activity board definition not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
