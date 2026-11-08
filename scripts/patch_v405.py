#!/usr/bin/env python3
"""Patch v404 -> v405: exclude system comments from post page chat count display"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v404.js'
dst = '_deploy/assets/index-DUcNPOLc-v405.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'children:[u.length,` Chats`]'
NEW = 'children:[u.filter(_c=>_c.username!==`__system__`).length,` Chats`]'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: system comments excluded from Chats count')
else:
    errors.append('FAIL: Chats count not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
