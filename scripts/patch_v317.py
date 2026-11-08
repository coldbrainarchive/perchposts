#!/usr/bin/env python3
"""Patch v316 -> v317: fix gap in comments with no reply.
margin-top on .chat-bubble-text adds space even when no quote bar exists.
Move spacing to margin-bottom on .chat-quote-bar so it only appears when a reply is present."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v316.js'
dst = '_deploy/assets/index-DUcNPOLc-v317.js'

content = open(src, encoding='utf-8').read()
errors = []

# Remove margin-top from bubble-text
OLD_TEXT = '.chat-bubble-text {\n        display: block;\n        white-space: pre-wrap;\n        margin-top: 8px;\n      }'
NEW_TEXT = '.chat-bubble-text {\n        display: block;\n        white-space: pre-wrap;\n      }'
if OLD_TEXT in content:
    content = content.replace(OLD_TEXT, NEW_TEXT, 1)
    print('OK: margin-top removed from .chat-bubble-text')
else:
    errors.append('FAIL: .chat-bubble-text not found')

# Add margin-bottom to quote bar instead
OLD_QUOTE = (
    '.chat-quote-bar {\n'
    '        margin: -6px -10px 0;\n'
    '        padding: 8px 12px;\n'
    '        border-radius: 0;\n'
    '        background: rgba(192,132,252,0.22);\n'
    '        border-bottom: 1px solid rgba(192,132,252,0.18);\n      }'
)
NEW_QUOTE = (
    '.chat-quote-bar {\n'
    '        margin: -6px -10px 8px;\n'   # 8px bottom margin = space to text below
    '        padding: 8px 12px;\n'
    '        border-radius: 0;\n'
    '        background: rgba(192,132,252,0.22);\n'
    '        border-bottom: 1px solid rgba(192,132,252,0.18);\n      }'
)
if OLD_QUOTE in content:
    content = content.replace(OLD_QUOTE, NEW_QUOTE, 1)
    print('OK: margin-bottom added to .chat-quote-bar — spacing only when reply exists')
else:
    errors.append('FAIL: .chat-quote-bar not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
