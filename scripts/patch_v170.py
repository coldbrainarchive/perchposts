#!/usr/bin/env python3
"""Patch v169 -> v170: hide header border when not logged in."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v169.js'
dst = '_deploy/assets/index-DUcNPOLc-v170.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'padding:`20px 18px 16px`,borderBottom:`1px solid #2e303a`,position:`relative`}'
NEW = 'padding:`20px 18px 16px`,borderBottom:e?`1px solid #2e303a`:`none`,position:`relative`}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: border hidden when not logged in')
else:
    errors.append('FAIL: header style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
