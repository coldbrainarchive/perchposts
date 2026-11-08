#!/usr/bin/env python3
"""Patch v512 -> v513: Fix mod purple in _UserCard pill and user filter in feed."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v512.js'
dst = '_deploy/assets/index-DUcNPOLc-v513.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Fix _UserCard hand-rolled pill to check is_mod / _modUsers ─────────────
# The card builds _col from Hn() but doesn't account for mods.
# We insert a resolved color variable before the return, then use it in the pill.
OLD_COL = ('const _col=Hn(_br?.browser_id||`_`,_un);')
NEW_COL = ('const _col=Hn(_br?.browser_id||`_`,_un);'
           'const _isMod=_br?.is_mod===true||(_un&&_modUsers.has(_un.toLowerCase())&&!(_br?.is_admin||(_un&&_adminUsers.has(_un.toLowerCase()))));'
           'const _resolvedCol=(_br?.is_admin||(_un&&_adminUsers.has(_un.toLowerCase())))?`#ffffff`:_isMod?`#c084fc`:_col;')
if OLD_COL in content:
    content = content.replace(OLD_COL, NEW_COL, 1)
    print('OK: _UserCard resolved color variable added')
else:
    errors.append('FAIL: _col declaration in _UserCard not found')

# ── 2. Use _resolvedCol in the pill instead of _col ──────────────────────────
OLD_PILL = ('className:`user-pill`,style:{color:`#0a0a0a`,'
            'background:_bd&&_bd.hat?`#ffffff`:_col,'
            'borderColor:_bd&&_bd.hat?`#e2e8f0`:_col,cursor:`default`,'
            'fontSize:_un&&_un.length>19?Math.max(7,Math.round(11*19/_un.length)):undefined},'
            'children:_un})')
NEW_PILL = ('className:`user-pill`,style:{color:_isMod?`#0a0a0a`:`#0a0a0a`,'
            'background:_bd&&_bd.hat?`#ffffff`:_resolvedCol,'
            'borderColor:_bd&&_bd.hat?`#e2e8f0`:_resolvedCol,cursor:`default`,'
            'fontSize:_un&&_un.length>19?Math.max(7,Math.round(11*19/_un.length)):undefined},'
            'children:_un})')
if OLD_PILL in content:
    content = content.replace(OLD_PILL, NEW_PILL, 1)
    print('OK: _UserCard pill uses resolved color')
else:
    errors.append('FAIL: _UserCard pill style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
