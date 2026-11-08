#!/usr/bin/env python3
"""Patch v319 -> v320: match reaction top gap to bubble top padding (both 6px)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v319.js'
dst = '_deploy/assets/index-DUcNPOLc-v320.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '        padding: 4px 10px 8px;\n        background: #1e2530;\n      }'
NEW = '        padding: 6px 10px 8px;\n        background: #1e2530;\n      }'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: reaction top padding set to 6px (matches bubble top padding)')
else:
    errors.append('FAIL: .chat-reactions padding not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
