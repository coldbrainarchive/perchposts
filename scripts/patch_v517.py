#!/usr/bin/env python3
"""Patch v516 -> v517:
- Remove _addMod from Jn() — causes stale cache from historical is_mod posts
- Fix _UserCard to only use _br?.is_mod (live record), not _modUsers cache
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v516.js'
dst = '_deploy/assets/index-DUcNPOLc-v517.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove _addMod call from Jn() ─────────────────────────────────────────
OLD_JN = ('if(e.is_admin){if(e.username)_addAdmin(e.username);return{e:null,f:``,s:null,hat:!0};}if(e.is_mod&&e.username)_addMod(e.username);')
NEW_JN = ('if(e.is_admin){if(e.username)_addAdmin(e.username);return{e:null,f:``,s:null,hat:!0};}')
if OLD_JN in content:
    content = content.replace(OLD_JN, NEW_JN, 1)
    print('OK: _addMod removed from Jn()')
else:
    errors.append('FAIL: Jn _addMod line not found')

# ── 2. Fix _UserCard: use only _br?.is_mod, drop _modUsers cache check ────────
OLD_ISMOD = ('const _isMod=_br?.is_mod===true||(_un&&_modUsers.has(_un.toLowerCase())&&!(_br?.is_admin||(_un&&_adminUsers.has(_un.toLowerCase()))));'
             'const _resolvedCol=(_br?.is_admin||(_un&&_adminUsers.has(_un.toLowerCase())))?`#ffffff`:_isMod?`#c084fc`:_col;')
NEW_ISMOD = ('const _isMod=_br?.is_mod===true&&!(_br?.is_admin||(_un&&_adminUsers.has(_un?.toLowerCase())));'
             'const _resolvedCol=(_br?.is_admin||(_un&&_adminUsers.has(_un?.toLowerCase())))?`#ffffff`:_isMod?`#c084fc`:_col;')
if OLD_ISMOD in content:
    content = content.replace(OLD_ISMOD, NEW_ISMOD, 1)
    print('OK: _UserCard uses only _br?.is_mod (no stale cache)')
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
