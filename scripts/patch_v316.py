#!/usr/bin/env python3
"""Patch v315 -> v316: fix quote bar width and text spacing in comment bubbles.
1. Quote bar: use negative margins (-6px -10px) to cancel bubble padding — stretches full width
2. Add margin-top to .chat-bubble-text so text has even breathing room below the quote bar"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v315.js'
dst = '_deploy/assets/index-DUcNPOLc-v316.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Quote bar: stretch full width with negative margins ────────────────────
OLD_QUOTE = (
    '.chat-quote-bar {\n        padding: 6px 12px;\n        margin-bottom: 0;\n'
    '        border-radius: 0;\n        background: rgba(192,132,252,0.22);\n'
    '        border-bottom: 1px solid rgba(192,132,252,0.18);\n      }'
)
NEW_QUOTE = (
    '.chat-quote-bar {\n'
    '        margin: -6px -10px 0;\n'   # cancel bubble padding, touch edges
    '        padding: 8px 12px;\n'      # own comfortable padding
    '        border-radius: 0;\n'
    '        background: rgba(192,132,252,0.22);\n'
    '        border-bottom: 1px solid rgba(192,132,252,0.18);\n      }'
)
if OLD_QUOTE in content:
    content = content.replace(OLD_QUOTE, NEW_QUOTE, 1)
    print('OK: quote bar stretched full width with negative margins')
else:
    errors.append('FAIL: .chat-quote-bar CSS not found')

# ── 2. Add spacing between quote bar and comment text ─────────────────────────
OLD_BUBBLE_TEXT = '.chat-bubble-text {\n        display: block;\n        white-space: pre-wrap;\n      }'
NEW_BUBBLE_TEXT = '.chat-bubble-text {\n        display: block;\n        white-space: pre-wrap;\n        margin-top: 8px;\n      }'
if OLD_BUBBLE_TEXT in content:
    content = content.replace(OLD_BUBBLE_TEXT, NEW_BUBBLE_TEXT, 1)
    print('OK: spacing added between quote bar and comment text')
else:
    errors.append('FAIL: .chat-bubble-text CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
