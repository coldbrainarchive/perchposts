#!/usr/bin/env python3
"""Patch v520 -> v521: Change USER label to BIRD in user card."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v520.js'
dst = '_deploy/assets/index-DUcNPOLc-v521.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.06em`},children:`USER`}'
NEW = 'fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.06em`},children:`BIRD`}'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: USER -> BIRD')
else:
    errors.append('FAIL: USER label not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
