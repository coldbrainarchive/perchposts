#!/usr/bin/env python3
"""Patch v346 -> v347: rename Questions board to Huddles with 👥 icon."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v346.js'
dst = '_deploy/assets/index-DUcNPOLc-v347.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '{name:`Questions`,slug:`feedback`,icon:`❔`}'
NEW = '{name:`Huddles`,slug:`feedback`,icon:`\U0001f465`}'

if OLD in content:
    content = content.replace(OLD, NEW)
    print('OK: Questions -> Huddles with 👥 icon')
else:
    errors.append('FAIL: Questions board entry not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
