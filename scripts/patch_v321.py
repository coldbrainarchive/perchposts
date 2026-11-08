#!/usr/bin/env python3
"""Patch v320 -> v321: fix reaction gap to match header gap.
Header->text = bubble padding-top (6px).
Text->emoji = bubble padding-bottom (6px) + reactions padding-top (6px) = 12px — too big.
Fix: set reactions padding-top to 0 so total = 6px, matching the top gap."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v320.js'
dst = '_deploy/assets/index-DUcNPOLc-v321.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '        padding: 6px 10px 8px;\n        background: #1e2530;\n      }'
NEW = '        padding: 0 10px 8px;\n        background: #1e2530;\n      }'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: reactions padding-top set to 0 — text→emoji gap now equals header→text gap')
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
