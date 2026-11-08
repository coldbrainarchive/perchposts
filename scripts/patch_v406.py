#!/usr/bin/env python3
"""Patch v405 -> v406: exclude system comments from 💬 count in post page action row"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v405.js'
dst = '_deploy/assets/index-DUcNPOLc-v406.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'children:`💬`}),(0,L.jsx)(`span`,{children:u.length})'
NEW = 'children:`💬`}),(0,L.jsx)(`span`,{children:u.filter(_c=>_c.username!==`__system__`).length})'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: 💬 count in post page excludes system comments')
else:
    errors.append('FAIL: post page 💬 count not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
