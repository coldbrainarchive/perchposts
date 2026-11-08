#!/usr/bin/env python3
"""Patch v426 -> v427:
Fix ":user" suffix appearing in huddle member pills.
Only append role suffix for admin/mod, not for regular "user" role.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v426.js'
dst = '_deploy/assets/index-DUcNPOLc-v427.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'huddle_members:_isHuddle?_hmTagged.map(_u=>_u.role?`${_u.username}:${_u.role}`:_u.username):[]'
NEW = 'huddle_members:_isHuddle?_hmTagged.map(_u=>(_u.role===`admin`||_u.role===`mod`)?`${_u.username}:${_u.role}`:_u.username):[]'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: only admin/mod get role suffix, plain users stay plain')
else:
    errors.append('FAIL: huddle_members map not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
