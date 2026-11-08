#!/usr/bin/env python3
"""Patch v350 -> v351:
- Board column: align-content flex-start so boards cluster at top
- Country drilldown: wrap in flex-wrap div so pills cluster into multiple rows
- Add max-height + overflow-y:auto to search-columns so it scrolls
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v350.js'
dst = '_deploy/assets/index-DUcNPOLc-v351.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add align-content:flex-start to boards column (in new post picker) ────
OLD_BOARDS_COL = (
    '!p&&(0,L.jsxs)(`div`,{className:`search-column`,children:['
    '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Boards`}),'
    'nr.filter(e=>!e.virtual).map('
)
NEW_BOARDS_COL = (
    '!p&&(0,L.jsxs)(`div`,{className:`search-column`,style:{alignContent:`flex-start`},children:['
    '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Boards`}),'
    'nr.filter(e=>!e.virtual).map('
)
if OLD_BOARDS_COL in content:
    content = content.replace(OLD_BOARDS_COL, NEW_BOARDS_COL, 1)
    print('OK: boards column align-content: flex-start')
else:
    errors.append('FAIL: boards column not found')

# ── 2. Wrap country drilldown pills in a flex-wrap div ────────────────────────
OLD_COUNTRY_LIST = (
    'or.filter(e=>ar[e.name]===S).map(e=>'
    '(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>{y(e.name);C(null);},'
    'style:{outline:`none`,boxShadow:e.name===v?`0 0 0 2px #c084fc`:`none`,borderRadius:999},'
    'children:(0,L.jsx)(kr,{country:e.name,small:!0})}'
    ',e.name))'
)
NEW_COUNTRY_LIST = (
    '(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:8,padding:`4px 0`},'
    'children:or.filter(e=>ar[e.name]===S).map(e=>'
    '(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>{y(e.name);C(null);},'
    'style:{outline:`none`,boxShadow:e.name===v?`0 0 0 2px #c084fc`:`none`,borderRadius:999},'
    'children:(0,L.jsx)(kr,{country:e.name,small:!0})}'
    ',e.name))})'
)
if OLD_COUNTRY_LIST in content:
    content = content.replace(OLD_COUNTRY_LIST, NEW_COUNTRY_LIST, 1)
    print('OK: country drilldown wrapped in flex-wrap div')
else:
    errors.append('FAIL: country drilldown list not found')

# ── 3. Add max-height + overflow to the search-columns container ──────────────
OLD_GRID = 'className:`search-columns`,children:[!p&&'
NEW_GRID = 'className:`search-columns`,style:{maxHeight:320,overflowY:`auto`},children:[!p&&'
if OLD_GRID in content:
    # Only replace the one in Ur (new post form), not the feed filter
    # Find Ur component first
    idx_ur = content.find('function Ur(')
    idx = content.find(OLD_GRID, idx_ur)
    if idx != -1:
        content = content[:idx] + content[idx:].replace(OLD_GRID, NEW_GRID, 1)
        print('OK: search-columns max-height + scroll added')
    else:
        errors.append('FAIL: search-columns in Ur not found')
else:
    errors.append('FAIL: search-columns className not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
