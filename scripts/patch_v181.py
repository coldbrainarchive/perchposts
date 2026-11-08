#!/usr/bin/env python3
"""Patch v180 -> v181: mod panel button uses accent purple #c084fc."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v180.js'
dst = '_deploy/assets/index-DUcNPOLc-v181.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'style:{display:`block`,padding:`12px 0`,borderRadius:12,'
    'background:`#7c3aed`,color:`#fff`,fontWeight:700,fontSize:14,'
    'cursor:`pointer`,textDecoration:`none`,textAlign:`center`},'
    'children:`Open Mod Panel`}'
)
NEW = (
    'style:{display:`block`,padding:`12px 0`,borderRadius:12,'
    'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,'
    'cursor:`pointer`,textDecoration:`none`,textAlign:`center`},'
    'children:`Open Mod Panel`}'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: mod panel button uses accent purple')
else:
    errors.append('FAIL: mod panel button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
