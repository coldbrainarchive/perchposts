#!/usr/bin/env python3
"""Patch v338 -> v340: segmented toggle, fixed className syntax (no backticks in ternary)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v338.js'
dst = '_deploy/assets/index-DUcNPOLc-v340.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Replace single toggle button with segmented control ───────────────────
OLD_BTN = (
    '(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:()=>{let e=D.current;e&&e.scrollTo({top:b?e.scrollHeight:0,behavior:`smooth`}),x(e=>!e)},'
    'children:b?`Newest`:`Oldest`})'
)
NEW_BTN = (
    '(0,L.jsxs)(`div`,{className:`sort-toggle`,children:['
    '(0,L.jsx)(`button`,{type:`button`,'
    'className:b?`sort-toggle-btn`:`sort-toggle-btn active`,'
    'onClick:()=>{if(b){let e=D.current;e&&e.scrollTo({top:0,behavior:`smooth`});x(!1);}},'
    'children:`Oldest`}),'
    '(0,L.jsx)(`button`,{type:`button`,'
    'className:b?`sort-toggle-btn active`:`sort-toggle-btn`,'
    'onClick:()=>{if(!b){let e=D.current;e&&e.scrollTo({top:e.scrollHeight,behavior:`smooth`});x(!0);}},'
    'children:`Newest`})'
    ']})'
)
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: segmented toggle JSX added')
else:
    errors.append('FAIL: Newest/Oldest button not found')

# ── 2. Add CSS for the segmented toggle ──────────────────────────────────────
OLD_CSS = '.chat-window {'
NEW_CSS = (
    '.sort-toggle {\n'
    '        display: flex;\n'
    '        border-radius: 999px;\n'
    '        border: 1px solid rgba(124,58,237,0.5);\n'
    '        overflow: hidden;\n'
    '        flex-shrink: 0;\n'
    '      }\n\n'
    '      .sort-toggle-btn {\n'
    '        padding: 0 10px;\n'
    '        height: 26px;\n'
    '        border: none;\n'
    '        background: transparent;\n'
    '        color: #94a3b8;\n'
    '        font-size: 11px;\n'
    '        font-weight: 700;\n'
    '        cursor: pointer;\n'
    '        transition: background 0.15s, color 0.15s;\n'
    '      }\n\n'
    '      .sort-toggle-btn.active {\n'
    '        background: #7c3aed;\n'
    '        color: #fff;\n'
    '      }\n\n'
    '      .chat-window {'
)
if OLD_CSS in content:
    content = content.replace(OLD_CSS, NEW_CSS, 1)
    print('OK: sort-toggle CSS added')
else:
    errors.append('FAIL: .chat-window CSS anchor not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
