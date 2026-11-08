#!/usr/bin/env python3
"""Patch v281 -> v282:
1. Fix country b.map (search results) still using old flag+text format — patch the 2nd occurrence
2. Fix admin badge in user search results — use _u.role instead of hardcoded is_admin:false
3. Fix admin badge in search bar user chip — look up role from UR array
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v281.js'
dst = '_deploy/assets/index-DUcNPOLc-v282.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Fix country suggestions in b.map (search results) ──────────────────────
OLD_BMAP = (
    'b.map(e=>(0,L.jsxs)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>k(e.name),children:[(0,L.jsx)(`span`,{className:`sugg-icon`,children:e.flag}),'
    '(0,L.jsx)(`span`,{className:`sugg-label`,children:e.name})]},e.name))'
)
NEW_BMAP = (
    'b.map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>k(e.name),children:(0,L.jsx)(kr,{country:e.name,small:!0})},e.name))'
)
if OLD_BMAP in content:
    content = content.replace(OLD_BMAP, NEW_BMAP, 1)
    print('OK: country b.map uses kr component')
else:
    errors.append('FAIL: country b.map not found')

# ── 2. Fix admin in user dropdown suggestions ─────────────────────────────────
OLD_USER_SUGG_XN = (
    'children:(0,L.jsx)(Xn,{record:{username:_u.username,is_admin:!1,is_mod:!1},'
    'name:_u.username,color:Hn(null,_u.username)})},_u.username)'
)
NEW_USER_SUGG_XN = (
    'children:(0,L.jsx)(Xn,{record:{username:_u.username,'
    'is_admin:_u.role===`admin`,is_mod:_u.role===`mod`},'
    'name:_u.username,color:_u.role===`admin`?`#ffffff`:Hn(null,_u.username)})},_u.username)'
)
if OLD_USER_SUGG_XN in content:
    content = content.replace(OLD_USER_SUGG_XN, NEW_USER_SUGG_XN, 1)
    print('OK: user suggestion uses role for admin/mod')
else:
    errors.append('FAIL: user suggestion Xn not found')

# ── 3. Fix admin in search bar user chip ──────────────────────────────────────
# Look up role from UR array (UR is in Lr scope)
OLD_USER_CHIP_XN = (
    'children:(0,L.jsx)(Xn,{record:{username:m,is_admin:!1,is_mod:!1},'
    'name:m,color:Hn(null,m)})'
)
NEW_USER_CHIP_XN = (
    'children:(0,L.jsx)(Xn,{record:{username:m,'
    'is_admin:(UR.find(_f=>_f.username===m)||{}).role===`admin`,'
    'is_mod:(UR.find(_f=>_f.username===m)||{}).role===`mod`},'
    'name:m,color:(UR.find(_f=>_f.username===m)||{}).role===`admin`?`#ffffff`:Hn(null,m)})'
)
if OLD_USER_CHIP_XN in content:
    content = content.replace(OLD_USER_CHIP_XN, NEW_USER_CHIP_XN, 1)
    print('OK: search bar user chip uses role for admin/mod')
else:
    errors.append('FAIL: search bar user chip Xn not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
