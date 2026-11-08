#!/usr/bin/env python3
"""Patch v518 -> v519: _UserCard uses live role from /user-stats instead of stale _br record."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v518.js'
dst = '_deploy/assets/index-DUcNPOLc-v519.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = ('const _isMod=_br?.is_mod===true&&!(_br?.is_admin||(_un&&_adminUsers.has(_un?.toLowerCase())));'
       'const _resolvedCol=(_br?.is_admin||(_un&&_adminUsers.has(_un?.toLowerCase())))?`#ffffff`:_isMod?`#c084fc`:_col;')
NEW = ('const _isAdmin=_s.role===`admin`||_br?.is_admin===true||(_un&&_adminUsers.has(_un?.toLowerCase()));'
       'const _isMod=_s.role===`mod`||(_br?.is_mod===true&&!_isAdmin);'
       'const _resolvedCol=_isAdmin?`#ffffff`:_isMod?`#c084fc`:_col;')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: _UserCard uses _s.role from /user-stats for colour')
else:
    errors.append('FAIL: _UserCard _isMod block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
