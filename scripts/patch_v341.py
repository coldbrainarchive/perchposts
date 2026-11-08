#!/usr/bin/env python3
"""Patch v340 -> v341: fix sort toggle purple to match app accent (#a855f7 / #c084fc)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v340.js'
dst = '_deploy/assets/index-DUcNPOLc-v341.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_CSS = (
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
    '      }'
)
NEW_CSS = (
    '.sort-toggle {\n'
    '        display: flex;\n'
    '        border-radius: 999px;\n'
    '        border: 1px solid #a855f7;\n'
    '        overflow: hidden;\n'
    '        flex-shrink: 0;\n'
    '      }\n\n'
    '      .sort-toggle-btn {\n'
    '        padding: 0 10px;\n'
    '        height: 26px;\n'
    '        border: none;\n'
    '        background: transparent;\n'
    '        color: #c084fc;\n'
    '        font-size: 11px;\n'
    '        font-weight: 700;\n'
    '        cursor: pointer;\n'
    '        transition: background 0.15s, color 0.15s;\n'
    '      }\n\n'
    '      .sort-toggle-btn.active {\n'
    '        background: #a855f7;\n'
    '        color: #fff;\n'
    '      }'
)
if OLD_CSS in content:
    content = content.replace(OLD_CSS, NEW_CSS, 1)
    print('OK: toggle purple updated to app accent (#a855f7)')
else:
    errors.append('FAIL: sort-toggle CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
