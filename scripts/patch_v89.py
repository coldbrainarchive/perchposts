#!/usr/bin/env python3
"""Patch v88 -> v89:
- Account tab username: remove @, add copy button
- Nav top-right: mobile shows only bird emoji (hide pill name)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v88.js'
dst = '_deploy/assets/index-DUcNPOLc-v89.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Account tab: remove @ and add copy button ──────────────────────────────
OLD_ACCOUNT = (
    '(0,L.jsxs)(`div`,{style:{padding:`9px 12px`,borderRadius:10,'
    'border:`1px solid #2e303a`,background:`#16171d`,color:`#94a3b8`,fontSize:14},'
    'children:[`@`,r||`—`]})'
)
NEW_ACCOUNT = (
    '(0,L.jsxs)(`div`,{style:{padding:`9px 12px`,borderRadius:10,'
    'border:`1px solid #2e303a`,background:`#16171d`,color:`#94a3b8`,fontSize:14,'
    'display:`flex`,alignItems:`center`,justifyContent:`space-between`},'
    'children:['
    'r||`—`,'
    'r&&(0,L.jsx)(`button`,{onClick:function(){try{navigator.clipboard.writeText(r)}catch(err){}},style:{background:`transparent`,border:`none`,cursor:`pointer`,color:`#64748b`,fontSize:15,padding:`0 2px`,lineHeight:1,flexShrink:0},children:`\U0001f4cb`})'
    ']})'
)

if OLD_ACCOUNT in content:
    content = content.replace(OLD_ACCOUNT, NEW_ACCOUNT, 1)
    print('OK: account tab username - removed @ and added copy button')
else:
    # Try with em-dash as actual char
    OLD_ACCOUNT2 = OLD_ACCOUNT.replace('—', '—')
    if OLD_ACCOUNT2 in content:
        content = content.replace(OLD_ACCOUNT2, NEW_ACCOUNT.replace('—', '—'), 1)
        print('OK: account tab username (em-dash variant) - removed @ and added copy button')
    else:
        # Show what's nearby
        idx = content.find('children:[`@`,r||')
        print('SEARCH:', idx, repr(content[idx:idx+80]) if idx != -1 else 'not found')
        errors.append('FAIL: account tab username display not found')

# ── 2. Nav button: add className for CSS targeting ────────────────────────────
OLD_NAV_BTN = (
    '(0,L.jsx)(`button`,{onClick:()=>{p(0),d(!0)},style:{background:`none`,'
    'border:`none`,padding:0,cursor:`pointer`,display:`flex`},children:'
)
NEW_NAV_BTN = (
    '(0,L.jsx)(`button`,{onClick:()=>{p(0),d(!0)},className:`nav-user-pill`,style:{background:`none`,'
    'border:`none`,padding:0,cursor:`pointer`,display:`flex`},children:'
)

if OLD_NAV_BTN in content:
    content = content.replace(OLD_NAV_BTN, NEW_NAV_BTN, 1)
    print('OK: nav button - added nav-user-pill class')
else:
    errors.append('FAIL: nav button not found')

# ── 3. Add CSS media query to hide pill name in nav on mobile ─────────────────
OLD_CSS = (
    '.user-pill-name {\n        max-width: 160px;\n        overflow: hidden;\n        tex'
)
NEW_CSS = (
    '.user-pill-name {\n        max-width: 160px;\n        overflow: hidden;\n        tex'
)

# Find and append media query after the existing user-pill-name closing brace
OLD_CSS_END = '.user-pill-name {\n        max-width: 160px;\n        overflow: hidden;\n        text-overflow: ellipsis;\n        white-space: nowrap;\n      }'
NEW_CSS_END = (
    '.user-pill-name {\n        max-width: 160px;\n        overflow: hidden;\n'
    '        text-overflow: ellipsis;\n        white-space: nowrap;\n      }\n\n'
    '      @media (max-width: 900px) {\n'
    '        .nav-user-pill .user-pill-name {\n'
    '          display: none;\n'
    '        }\n'
    '      }'
)

if OLD_CSS_END in content:
    content = content.replace(OLD_CSS_END, NEW_CSS_END, 1)
    print('OK: CSS - added mobile media query to hide nav pill name')
else:
    errors.append('FAIL: user-pill-name CSS block not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
