#!/usr/bin/env python3
"""Patch v282 -> v283:
1. Replace Xn with consistent inline pill for user dropdown suggestions (matches Ar/kr height)
2. Replace Xn with inline pill for search bar user chip
3. Increase gap between tags in search-column
4. More space between sections (search-divider margin)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v282.js'
dst = '_deploy/assets/index-DUcNPOLc-v283.js'

content = open(src, encoding='utf-8').read()
errors = []

# Inline user pill template — same height/shape as Ar/kr, uses bird emoji + username
# Admin: white background + hat bird image; others: colored background + bird emoji
def _user_pill(uname_expr, role_expr, jn_expr):
    return (
        '(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4,'
        'height:22,padding:`0 7px`,borderRadius:999,'
        'border:`1px solid rgba(0,0,0,0.15)`,'
        f'background:{role_expr}===`admin`?`#ffffff`:Hn(null,{uname_expr}),'
        'color:`#0a0a0a`,fontSize:10,fontWeight:800,'
        'letterSpacing:`0.03em`,textTransform:`uppercase`,'
        'whiteSpace:`nowrap`,lineHeight:1,flexShrink:0,boxSizing:`border-box`},'
        f'children:[{role_expr}===`admin`'
        f'?(0,L.jsx)(`img`,{{src:`/admin-bird.png`,style:{{height:14,width:`auto`,display:`block`}}}})'
        f':(0,L.jsx)(`span`,{{children:(Jn({{username:{uname_expr},browser_id:null}})||{{}}).e||`🐦`}}),'
        f'(0,L.jsx)(`span`,{{children:{uname_expr}}})'
        ']})'
    )

# ── 1. User dropdown suggestion: replace Xn with inline pill ─────────────────
OLD_SUGG_XN = (
    'children:(0,L.jsx)(Xn,{record:{username:_u.username,'
    'is_admin:_u.role===`admin`,is_mod:_u.role===`mod`},'
    'name:_u.username,color:_u.role===`admin`?`#ffffff`:Hn(null,_u.username)})},_u.username)'
)
NEW_SUGG_XN = 'children:' + _user_pill('_u.username', '_u.role', 'Jn') + '},_u.username)'
if OLD_SUGG_XN in content:
    content = content.replace(OLD_SUGG_XN, NEW_SUGG_XN, 1)
    print('OK: user suggestion uses inline pill')
else:
    errors.append('FAIL: user suggestion Xn not found')

# ── 2. Search bar user chip: replace Xn with inline pill ─────────────────────
_ROLE_EXPR = '(UR.find(_f=>_f.username===m)||{}).role'
OLD_CHIP_XN = (
    'children:(0,L.jsx)(Xn,{record:{username:m,'
    f'is_admin:{_ROLE_EXPR}===`admin`,'
    f'is_mod:{_ROLE_EXPR}===`mod`}},'
    f'name:m,color:{_ROLE_EXPR}===`admin`?`#ffffff`:Hn(null,m)}})'
)
NEW_CHIP_XN = 'children:' + _user_pill('m', _ROLE_EXPR, 'Jn')
if OLD_CHIP_XN in content:
    content = content.replace(OLD_CHIP_XN, NEW_CHIP_XN, 1)
    print('OK: search bar user chip uses inline pill')
else:
    errors.append('FAIL: search bar user chip Xn not found')

# ── 3. Increase gap in search-column from 5px to 8px ─────────────────────────
OLD_COL_CSS = (
    '.search-column {\n        display: flex;\n        flex-wrap: wrap;\n'
    '        gap: 5px;\n        align-items: center;\n      }'
)
NEW_COL_CSS = (
    '.search-column {\n        display: flex;\n        flex-wrap: wrap;\n'
    '        gap: 8px;\n        align-items: center;\n      }'
)
if OLD_COL_CSS in content:
    content = content.replace(OLD_COL_CSS, NEW_COL_CSS, 1)
    print('OK: search-column gap increased to 8px')
else:
    errors.append('FAIL: search-column CSS not found')

# ── 4. Increase search-divider margin for more breathing room ─────────────────
OLD_DIV = '.search-divider { height: 1px; background: #374151; margin: 4px 0; }'
NEW_DIV = '.search-divider { height: 1px; background: #374151; margin: 8px 0; }'
if OLD_DIV in content:
    content = content.replace(OLD_DIV, NEW_DIV, 1)
    print('OK: search-divider margin increased')
else:
    print('NOTE: search-divider not found — skipping')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
