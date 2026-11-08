#!/usr/bin/env python3
"""Patch v208 -> v209: country/continent chip → light grey."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v208.js'
dst = '_deploy/assets/index-DUcNPOLc-v209.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = "background:`#f59e0b`"
NEW = "background:`#cbd5e1`"

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: country chip → light grey')
else:
    errors.append('FAIL: country chip colour not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
