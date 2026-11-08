#!/usr/bin/env python3
"""Patch v182 -> v183: mod pill = accent purple, admin pill = white."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v182.js'
dst = '_deploy/assets/index-DUcNPOLc-v183.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'color:`#0a0a0a`,background:D?`#ffffff`:A,borderColor:D?`#e2e8f0`:A,cursor:`default`'
NEW = (
    'color:`#0a0a0a`,'
    'background:t===`admin`?`#ffffff`:t===`mod`?`#c084fc`:A,'
    'borderColor:t===`admin`?`#e2e8f0`:t===`mod`?`#a855f7`:A,'
    'cursor:`default`'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: mod=purple, admin=white in panel header pill')
else:
    errors.append('FAIL: header pill style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
