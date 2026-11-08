#!/usr/bin/env python3
"""Patch v505 -> v506: OP can only pin their own comments, not other users'."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v505.js'
dst = '_deploy/assets/index-DUcNPOLc-v506.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'canPin:N||(c.is_huddle&&n&&c.username&&n.toLowerCase()===c.username.toLowerCase())'
NEW = 'canPin:N||(c.is_huddle&&n&&c.username&&n.toLowerCase()===c.username.toLowerCase()&&e.username&&e.username.toLowerCase()===n.toLowerCase())'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: OP canPin restricted to own comments')
else:
    errors.append('FAIL: canPin condition not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
