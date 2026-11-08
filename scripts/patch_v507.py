#!/usr/bin/env python3
"""Patch v506 -> v507: Reduce height of colored comment header bar."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v506.js'
dst = '_deploy/assets/index-DUcNPOLc-v507.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '.chat-msg-meta {\n        display: flex;\n        align-items: center;\n        gap: 6px;\n        padding: 5px 10px;\n      }'
NEW = '.chat-msg-meta {\n        display: flex;\n        align-items: center;\n        gap: 6px;\n        padding: 3px 10px;\n      }'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: chat-msg-meta padding reduced to 3px 10px')
else:
    errors.append('FAIL: chat-msg-meta style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
