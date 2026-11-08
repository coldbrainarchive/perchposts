#!/usr/bin/env python3
"""Patch v321 -> v322: add bottom breathing room when no reactions exist.
Use :has() to target bubble only when no .chat-reactions or .chat-action-sheet follows."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v321.js'
dst = '_deploy/assets/index-DUcNPOLc-v322.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_BUBBLE = (
    '.chat-bubble {\n        background: #1e2530;\n        color: #dbe4ee;\n'
    '        border-radius: 0;\n        padding: 6px 10px;\n'
)
NEW_BUBBLE = (
    '.chat-bubble {\n        background: #1e2530;\n        color: #dbe4ee;\n'
    '        border-radius: 0;\n        padding: 6px 10px;\n'
    '      }\n\n'
    '      .chat-msg-body:not(:has(.chat-reactions)):not(:has(.chat-action-sheet)) .chat-bubble {\n'
    '        padding-bottom: 12px;\n'
    '      }\n\n'
    '      .chat-bubble-extra {\n'  # placeholder to keep structure intact
    '        display: none;\n'
    '      }\n\n'
    '      .chat-bubble-unused {\n'  # remove placeholders
    '        display: none;\n'
    # Actually don't add placeholders, just open the real rule again
)

# Simpler approach: just inject the :has() rule right after the .chat-bubble rule
OLD_BUBBLE2 = (
    '.chat-bubble {\n        background: #1e2530;\n        color: #dbe4ee;\n'
    '        border-radius: 0;\n        padding: 6px 10px;\n        font-size: 13px;\n'
    '        line-height: 1.4;\n        cursor: pointer;\n'
    '        word-break: break-word;\n        transition: opacity 0.15s;\n      }'
)
NEW_BUBBLE2 = (
    '.chat-bubble {\n        background: #1e2530;\n        color: #dbe4ee;\n'
    '        border-radius: 0;\n        padding: 6px 10px;\n        font-size: 13px;\n'
    '        line-height: 1.4;\n        cursor: pointer;\n'
    '        word-break: break-word;\n        transition: opacity 0.15s;\n      }\n\n'
    '      .chat-msg-body:not(:has(.chat-reactions)):not(:has(.chat-action-sheet)) .chat-bubble {\n'
    '        padding-bottom: 12px;\n      }'
)
if OLD_BUBBLE2 in content:
    content = content.replace(OLD_BUBBLE2, NEW_BUBBLE2, 1)
    print('OK: padding-bottom:12px added to bubble when no reactions/actions present')
else:
    errors.append('FAIL: .chat-bubble block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
