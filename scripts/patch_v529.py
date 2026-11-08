#!/usr/bin/env python3
"""Patch v528 -> v529: Remove duplicate flex:1 from HATCHED columns in both panels."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v528.js'
dst = '_deploy/assets/index-DUcNPOLc-v529.js'

content = open(src, encoding='utf-8').read()
errors = []

# Both panels have the same duplicate — replace all occurrences
OLD = 'flex:1,flex:1,display:`flex`'
NEW = 'flex:1,display:`flex`'
count = content.count(OLD)
if count > 0:
    content = content.replace(OLD, NEW)
    print(f'OK: duplicate flex:1 removed ({count} occurrences)')
else:
    errors.append('FAIL: duplicate flex:1 not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
