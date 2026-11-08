#!/usr/bin/env python3
"""Patch v378 -> v379:
- Leave huddle navigates to main feed (/) instead of /huddles
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v378.js'
dst = '_deploy/assets/index-DUcNPOLc-v379.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'if(_r.ok){window.location.href=`/huddles`;}'
NEW = 'if(_r.ok){window.location.href=`/`;}'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: leave navigates to main feed')
else:
    errors.append('FAIL: leave nav not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
