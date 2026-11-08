#!/usr/bin/env python3
"""Patch v253 -> v254: pass is_admin/is_mod from inbox data into Xn record."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v253.js'
dst = '_deploy/assets/index-DUcNPOLc-v254.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '(0,L.jsx)(Xn,{record:{username:_cv.contact},name:_cv.contact,color:Hn(null,_cv.contact)})'
NEW = '(0,L.jsx)(Xn,{record:{username:_cv.contact,is_admin:!!_cv.is_admin,is_mod:!!_cv.is_mod},name:_cv.contact,color:_cv.is_admin?`#ffffff`:Hn(null,_cv.contact)})'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: is_admin/is_mod passed to Xn in inbox rows')
else:
    errors.append('FAIL: Xn call not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
