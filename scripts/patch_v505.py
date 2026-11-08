#!/usr/bin/env python3
"""Patch v504 -> v505: Remove purple left border from pinned comment bubbles."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v504.js'
dst = '_deploy/assets/index-DUcNPOLc-v505.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'e.pinned?{borderLeft:`2px solid rgba(192,132,252,0.5)`,background:`rgba(192,132,252,0.06)`,paddingLeft:10}:void 0'
NEW = 'e.pinned?{background:`rgba(192,132,252,0.06)`}:void 0'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: purple left border removed from pinned bubbles')
else:
    errors.append('FAIL: pinned bubble style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
