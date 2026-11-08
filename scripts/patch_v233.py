#!/usr/bin/env python3
"""Patch v232 -> v233: remove purple bubble override for own comments (keep right-align only)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v232.js'
dst = '_deploy/assets/index-DUcNPOLc-v233.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_CSS = (
    '      .chat-msg--mine .chat-bubble {\n'
    '        background: #3b1f6e;\n'
    '        color: #f3e8ff;\n'
    '      }'
)
NEW_CSS = ''

if OLD_CSS in content:
    content = content.replace(OLD_CSS, NEW_CSS, 1)
    print('OK: purple bubble CSS removed')
else:
    errors.append('FAIL: purple bubble CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
