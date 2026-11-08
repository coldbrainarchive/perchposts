#!/usr/bin/env python3
"""Patch v322 -> v323: match action buttons to reaction pill size (20px h, 11px font)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v322.js'
dst = '_deploy/assets/index-DUcNPOLc-v323.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '.chat-action-btn {\n        height: 26px;\n        padding: 0 10px;\n'
    '        border-radius: 999px;\n        border: 1px solid rgba(148,163,184,0.2);\n'
    '        background: transparent;\n        color: #94a3b8;\n        font-size: 12px;\n'
    '        font-weight: 70'
)
NEW = (
    '.chat-action-btn {\n        height: 20px;\n        padding: 0 7px;\n'
    '        border-radius: 999px;\n        border: 1px solid rgba(148,163,184,0.2);\n'
    '        background: transparent;\n        color: #94a3b8;\n        font-size: 11px;\n'
    '        font-weight: 70'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: action buttons matched to pill size (20px, 11px)')
else:
    errors.append('FAIL: .chat-action-btn not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
