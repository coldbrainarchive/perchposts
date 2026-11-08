#!/usr/bin/env python3
"""Patch v324 -> v327: emoji picker input styled like action buttons (20px pill, transparent bg)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v324.js'
dst = '_deploy/assets/index-DUcNPOLc-v327.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Row CSS: add padding to match action sheet spacing ─────────────────────
OLD_ROW = '.chat-emoji-picker-row {\n        margin-top: 5px;\n      }'
NEW_ROW = '.chat-emoji-picker-row {\n        padding: 6px 10px 8px;\n      }'
if OLD_ROW in content:
    content = content.replace(OLD_ROW, NEW_ROW, 1)
    print('OK: emoji picker row padding set')
else:
    errors.append('FAIL: .chat-emoji-picker-row CSS not found')

# ── 2. Input CSS: match action button style ───────────────────────────────────
OLD_INPUT = (
    '.chat-emoji-picker-input {\n'
    '        height: 30px;\n'
    '        padding: 0 12px;\n'
    '        border-radius: 999px;\n'
    '        border: 1px solid rgba(148,163,184,0.25);\n'
    '        background: #0f1117;\n'
    '        color: #f8fafc;\n'
    '        font-size: 16px;\n'
    '        outline: none;\n'
    '        width: 140px;\n'
    '      }'
)
NEW_INPUT = (
    '.chat-emoji-picker-input {\n'
    '        height: 20px;\n'
    '        padding: 0 7px;\n'
    '        border-radius: 999px;\n'
    '        border: 1px solid rgba(148,163,184,0.2);\n'
    '        background: transparent;\n'
    '        color: #94a3b8;\n'
    '        font-size: 11px;\n'
    '        font-weight: 700;\n'
    '        outline: none;\n'
    '        width: auto;\n'
    '      }'
)
if OLD_INPUT in content:
    content = content.replace(OLD_INPUT, NEW_INPUT, 1)
    print('OK: emoji input styled as action button pill')
else:
    errors.append('FAIL: .chat-emoji-picker-input CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
