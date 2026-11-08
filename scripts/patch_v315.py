#!/usr/bin/env python3
"""Patch v314 -> v315: restore background on chat-reactions and chat-action-sheet.
The DM changes stripped background:#1e2530 from both, making them transparent in
comments — they now float over the page background instead of staying inside the card.
Restore the background to the base classes. DM context already has its own scoped
padding overrides; add background:transparent override for .dm-outer to keep DMs clean."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v314.js'
dst = '_deploy/assets/index-DUcNPOLc-v315.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Restore background to .chat-reactions ──────────────────────────────────
OLD_RX = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n'
    '        gap: 4px;\n        padding: 4px 10px 6px;\n      }'
)
NEW_RX = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n'
    '        gap: 4px;\n        padding: 0 14px 8px;\n        background: #1e2530;\n      }\n\n'
    '      .dm-outer .chat-reactions {\n        background: transparent;\n        padding: 4px 10px 6px;\n      }'
)
if OLD_RX in content:
    content = content.replace(OLD_RX, NEW_RX, 1)
    print('OK: .chat-reactions background restored; .dm-outer override added')
else:
    errors.append('FAIL: .chat-reactions CSS not found')

# ── 2. Restore background to .chat-action-sheet ───────────────────────────────
OLD_ACTION = (
    '.chat-action-sheet {\n        display: flex;\n        gap: 5px;\n'
    '        flex-wrap: wrap;\n        padding: 6px 10px 8px;\n'
    '        border-top: 1px solid rgba(148,163,184,0.12);\n      }'
)
NEW_ACTION = (
    '.chat-action-sheet {\n        display: flex;\n        gap: 6px;\n'
    '        flex-wrap: wrap;\n        padding: 8px 14px;\n'
    '        background: #1e2530;\n        border-top: 1px solid rgba(148,163,184,0.1);\n      }\n\n'
    '      .dm-outer .chat-action-sheet {\n        background: transparent;\n'
    '        padding: 5px 0 0;\n        border-top: none;\n      }'
)
if OLD_ACTION in content:
    content = content.replace(OLD_ACTION, NEW_ACTION, 1)
    print('OK: .chat-action-sheet background restored; .dm-outer override added')
else:
    errors.append('FAIL: .chat-action-sheet CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
