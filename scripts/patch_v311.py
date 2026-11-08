#!/usr/bin/env python3
"""Patch v310 -> v311: fix comment compose definitively.
The comment section is a window-scroll page, not a bounded container.
position:sticky isn't reliably sticking because of the flex ancestor with overflow:hidden.
Fix: scope .comments-shell .chat-compose to position:fixed bottom:0 — always visible.
Add padding-bottom to .comments-shell so last comments aren't hidden under compose."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v310.js'
dst = '_deploy/assets/index-DUcNPOLc-v311.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add padding-bottom to .comments-shell + scoped compose rule ────────────
OLD_COMMENTS_SHELL = '.comments-shell {\n        margin-top: 18px;\n      }'
NEW_COMMENTS_SHELL = (
    '.comments-shell {\n        margin-top: 18px;\n        padding-bottom: 80px;\n      }\n\n'
    '      .comments-shell .chat-compose {\n'
    '        position: fixed;\n'
    '        bottom: 0;\n'
    '        left: 0;\n'
    '        right: 0;\n'
    '        z-index: 50;\n'
    '        padding-bottom: max(10px, env(safe-area-inset-bottom, 0px));\n'
    '      }'
)
if OLD_COMMENTS_SHELL in content:
    content = content.replace(OLD_COMMENTS_SHELL, NEW_COMMENTS_SHELL, 1)
    print('OK: comment compose fixed to viewport bottom; padding-bottom added to comments-shell')
else:
    errors.append('FAIL: .comments-shell CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
