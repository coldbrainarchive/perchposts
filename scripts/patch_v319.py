#!/usr/bin/env python3
"""Patch v318 -> v319: smaller reaction pills, better left alignment.
- Align reactions with bubble text (10px left padding, matches bubble's 10px)
- Reduce pill height 24px -> 20px, font-size 13px -> 11px, gap 3px -> 2px"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v318.js'
dst = '_deploy/assets/index-DUcNPOLc-v319.js'

content = open(src, encoding='utf-8').read()
errors = []

# Fix left alignment: 14px -> 10px to match bubble padding
OLD_RX = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n'
    '        gap: 4px;\n        padding: 0 14px 8px;\n        background: #1e2530;\n      }'
)
NEW_RX = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n'
    '        gap: 4px;\n        padding: 4px 10px 8px;\n        background: #1e2530;\n      }'
)
if OLD_RX in content:
    content = content.replace(OLD_RX, NEW_RX, 1)
    print('OK: reaction left padding aligned to 10px (matches bubble text)')
else:
    errors.append('FAIL: .chat-reactions not found')

# Smaller pills: height 24->20, font-size 13->11, gap 3->2, padding tighter
OLD_PILL = (
    '.chat-reaction-pill {\n        display: inline-flex;\n        align-items: center;\n'
    '        gap: 3px;\n        height: 24px;\n        padding: 0 8px;\n'
    '        border-radius: 999px;\n        border: 1px solid rgba(148,163,184,0.2);\n'
    '        background: rgba(148,163,184,0.07);\n        font-size: 13px;\n'
)
NEW_PILL = (
    '.chat-reaction-pill {\n        display: inline-flex;\n        align-items: center;\n'
    '        gap: 2px;\n        height: 20px;\n        padding: 0 7px;\n'
    '        border-radius: 999px;\n        border: 1px solid rgba(148,163,184,0.2);\n'
    '        background: rgba(148,163,184,0.07);\n        font-size: 11px;\n'
)
if OLD_PILL in content:
    content = content.replace(OLD_PILL, NEW_PILL, 1)
    print('OK: reaction pills smaller (20px height, 11px font)')
else:
    errors.append('FAIL: .chat-reaction-pill not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
