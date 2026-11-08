#!/usr/bin/env python3
"""Patch v280 -> v281: make search dropdown suggestions and bar chips use Ar/kr/Xn
components so they visually match postcard tags. Update layout CSS for flex-wrap pills."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v280.js'
dst = '_deploy/assets/index-DUcNPOLc-v281.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── CSS: search-columns → flex column, search-column → flex-wrap row ──────────
OLD_CSS_COLUMNS = (
    '.search-columns {\n        display: grid;\n        grid-template-columns: 1fr 1fr;\n        gap: 0;\n      }'
)
NEW_CSS_COLUMNS = (
    '.search-columns {\n        display: flex;\n        flex-direction: column;\n        gap: 8px;\n        padding: 8px 14px;\n      }'
)
if OLD_CSS_COLUMNS in content:
    content = content.replace(OLD_CSS_COLUMNS, NEW_CSS_COLUMNS, 1)
    print('OK: search-columns CSS updated')
else:
    errors.append('FAIL: search-columns CSS not found')

OLD_CSS_COLUMN = '.search-column {\n        min-width: 0;\n      }'
NEW_CSS_COLUMN = (
    '.search-column {\n        display: flex;\n        flex-wrap: wrap;\n        gap: 5px;\n        align-items: center;\n      }'
)
if OLD_CSS_COLUMN in content:
    content = content.replace(OLD_CSS_COLUMN, NEW_CSS_COLUMN, 1)
    print('OK: search-column CSS updated')
else:
    errors.append('FAIL: search-column CSS not found')

# section label: full-width in flex-wrap context + remove excess padding
OLD_CSS_LABEL = '.search-section-label {\n        padding: 8px 14px 3px;\n        font-size: 10px;\n        font-weight: 700;\n        color: #4b5563;\n        text-transform: uppercase;\n        letter-spacing: 0.08em;\n      }'
NEW_CSS_LABEL = (
    '.search-section-label {\n        flex-basis: 100%;\n        padding: 0 0 1px;\n        font-size: 10px;\n        font-weight: 700;\n        color: #4b5563;\n        text-transform: uppercase;\n        letter-spacing: 0.08em;\n      }'
)
if OLD_CSS_LABEL in content:
    content = content.replace(OLD_CSS_LABEL, NEW_CSS_LABEL, 1)
    print('OK: search-section-label CSS updated')
else:
    print('NOTE: search-section-label CSS not found — skipping')

# search-suggestion → invisible button wrapper (Ar/kr/Xn provide all visual style)
OLD_CSS_SUGGESTION = (
    '.search-suggestion {\n        display: flex;\n        align-items: center;\n        gap: 10px;\n        width: 100%;\n        padding: 7px 14px;\n        background: none;\n        border: none;\n        color: #e2e8f0;\n        font-size: 13px;\n        cursor: pointer;\n        text-align: left;\n      }'
)
NEW_CSS_SUGGESTION = (
    '.search-suggestion {\n        background: none;\n        border: none;\n        padding: 0;\n        cursor: pointer;\n        display: inline-flex;\n        flex-shrink: 0;\n      }\n      .search-suggestion:hover { opacity: 0.82; }'
)
if OLD_CSS_SUGGESTION in content:
    content = content.replace(OLD_CSS_SUGGESTION, NEW_CSS_SUGGESTION, 1)
    print('OK: search-suggestion CSS updated')
else:
    errors.append('FAIL: search-suggestion CSS not found')

# search-chip → invisible wrapper (Ar/kr/Xn provide visual style)
OLD_CSS_CHIP = (
    '.search-chip {\n        display: inline-flex;\n        align-items: center;\n        gap: 5px;\n        height: 22px;\n        padding: 0 7px;\n        border-radius: 999px;\n        background: rgba(192,132,252,0.15);\n        border: 1px solid rgba(192,132,252,0.4);\n        color: #c084fc;\n        font-size: 10px;\n        font-weight: 800;\n        letter-spacing: 0.03em;\n        text-transform: uppercase;\n        white-space: nowrap;\n        flex-shrink: 0;\n        line-height: 1;\n        overflow: hidden;\n        box-sizing: border-box;\n      }'
)
NEW_CSS_CHIP = (
    '.search-chip {\n        background: none;\n        border: none;\n        padding: 0;\n        cursor: pointer;\n        display: inline-flex;\n        flex-shrink: 0;\n      }'
)
if OLD_CSS_CHIP in content:
    content = content.replace(OLD_CSS_CHIP, NEW_CSS_CHIP, 1)
    print('OK: search-chip CSS updated')
else:
    errors.append('FAIL: search-chip CSS not found')

# ── Search bar chips: replace with Ar/kr/Xn wrappers ─────────────────────────
OLD_BOARD_CHIP = (
    'board-chip`,onClick:e=>{e.stopPropagation(),A()},children:[(0,L.jsx)(`span`,{children:j.icon}),(0,L.jsx)(`span`,{children:j.name})]'
)
NEW_BOARD_CHIP = (
    'board-chip`,onClick:e=>{e.stopPropagation(),A()},style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(Ar,{boardName:j.name,small:!0})'
)
if OLD_BOARD_CHIP in content:
    content = content.replace(OLD_BOARD_CHIP, NEW_BOARD_CHIP, 1)
    print('OK: board chip uses Ar component')
else:
    errors.append('FAIL: board chip not found')

OLD_CONTINENT_CHIP = (
    'continent-chip`,onClick:e=>{e.stopPropagation(),te()},children:[(0,L.jsx)(`span`,{children:Or[f]||`🌐`}),(0,L.jsx)(`span`,{children:f})]'
)
NEW_CONTINENT_CHIP = (
    'continent-chip`,onClick:e=>{e.stopPropagation(),te()},style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(kr,{continent:f,small:!0})'
)
if OLD_CONTINENT_CHIP in content:
    content = content.replace(OLD_CONTINENT_CHIP, NEW_CONTINENT_CHIP, 1)
    print('OK: continent chip uses kr component')
else:
    errors.append('FAIL: continent chip not found')

OLD_COUNTRY_CHIP = (
    'country-chip`,onClick:e=>{e.stopPropagation(),ne()},children:[(0,L.jsxs)(`span`,{children:[ir(p),` `,p]})]'
)
NEW_COUNTRY_CHIP = (
    'country-chip`,onClick:e=>{e.stopPropagation(),ne()},style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(kr,{country:p,small:!0})'
)
if OLD_COUNTRY_CHIP in content:
    content = content.replace(OLD_COUNTRY_CHIP, NEW_COUNTRY_CHIP, 1)
    print('OK: country chip uses kr component')
else:
    errors.append('FAIL: country chip not found')

OLD_USER_CHIP = (
    'search-chip`,style:{background:`rgba(192,132,252,0.15)`,borderColor:`#c084fc55`,color:`#c084fc`},onClick:e=>{e.stopPropagation(),re()},children:[(0,L.jsxs)(`span`,{children:[`👤 `,m]})]'
)
NEW_USER_CHIP = (
    'search-chip`,onClick:e=>{e.stopPropagation(),re()},style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(Xn,{record:{username:m,is_admin:!1,is_mod:!1},name:m,color:Hn(null,m)})'
)
if OLD_USER_CHIP in content:
    content = content.replace(OLD_USER_CHIP, NEW_USER_CHIP, 1)
    print('OK: user chip uses Xn component')
else:
    errors.append('FAIL: user chip not found')

# ── Dropdown suggestions: replace with Ar/kr/Xn ──────────────────────────────
OLD_BOARD_SUGG = (
    'className:`search-suggestion`,type:`button`,onClick:()=>ee(e.slug),children:[(0,L.jsx)(`span`,{className:`sugg-icon`,children:e.icon}),(0,L.jsx)(`span`,{className:`sugg-label`,children:e.name})]},e.slug)'
)
NEW_BOARD_SUGG = (
    'className:`search-suggestion`,type:`button`,onClick:()=>ee(e.slug),children:(0,L.jsx)(Ar,{boardName:e.name,small:!0})},e.slug)'
)
if OLD_BOARD_SUGG in content:
    content = content.replace(OLD_BOARD_SUGG, NEW_BOARD_SUGG, 1)
    print('OK: board suggestions use Ar component')
else:
    errors.append('FAIL: board suggestion not found')

OLD_REGION_SUGG = (
    'className:`search-suggestion`,type:`button`,onClick:()=>{D(e),e!==`World`&&O(e)},children:[(0,L.jsx)(`span`,{className:`sugg-icon`,children:`🌍`}),(0,L.jsx)(`span`,{className:`sugg-label`,children:e})]},e)'
)
NEW_REGION_SUGG = (
    'className:`search-suggestion`,type:`button`,onClick:()=>{D(e),e!==`World`&&O(e)},children:(0,L.jsx)(kr,{continent:e,small:!0})},e)'
)
if OLD_REGION_SUGG in content:
    content = content.replace(OLD_REGION_SUGG, NEW_REGION_SUGG, 1)
    print('OK: region suggestions use kr component')
else:
    errors.append('FAIL: region suggestion not found')

OLD_COUNTRY_SUGG = (
    'className:`search-suggestion`,type:`button`,onClick:()=>k(e.name),children:[(0,L.jsx)(`span`,{className:`sugg-icon`,children:e.flag}),(0,L.jsx)(`span`,{className:`sugg-label`,children:e.name})]},e.name)'
)
NEW_COUNTRY_SUGG = (
    'className:`search-suggestion`,type:`button`,onClick:()=>k(e.name),children:(0,L.jsx)(kr,{country:e.name,small:!0})},e.name)'
)
if OLD_COUNTRY_SUGG in content:
    content = content.replace(OLD_COUNTRY_SUGG, NEW_COUNTRY_SUGG, 1)
    print('OK: country suggestions use kr component')
else:
    errors.append('FAIL: country suggestion not found')

OLD_USER_SUGG = (
    'className:`search-suggestion`,type:`button`,'
    'onClick:()=>{a(!1);setUR([]);window.location.href=`/?user=${encodeURIComponent(_u.username)}`;},'
    'children:[(0,L.jsx)(`span`,{className:`sugg-icon`,children:(Jn({username:_u.username,browser_id:null})||{}).e||`🐦`}),'
    '(0,L.jsx)(`span`,{className:`sugg-label`,children:_u.username})]},_u.username)'
)
NEW_USER_SUGG = (
    'className:`search-suggestion`,type:`button`,'
    'onClick:()=>{a(!1);setUR([]);window.location.href=`/?user=${encodeURIComponent(_u.username)}`;},'
    'children:(0,L.jsx)(Xn,{record:{username:_u.username,is_admin:!1,is_mod:!1},name:_u.username,color:Hn(null,_u.username)})},_u.username)'
)
if OLD_USER_SUGG in content:
    content = content.replace(OLD_USER_SUGG, NEW_USER_SUGG, 1)
    print('OK: user suggestions use Xn component')
else:
    errors.append('FAIL: user suggestion not found')

# ── Also remove padding from search-columns container in JSX (CSS handles it now) ─
# The columns div currently has no inline padding; CSS .search-columns adds it.
# But remove the padding from search-column labels that were inside each column.
# Section labels inside columns had padding:8px 14px 3px — now CSS uses 0 0 1px.
# (Already handled by CSS change above)

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
