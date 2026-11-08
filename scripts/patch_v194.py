#!/usr/bin/env python3
"""Patch v193 -> v194: OP badge colour → black."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v193.js'
dst = '_deploy/assets/index-DUcNPOLc-v194.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '.comment-card-op {\n'
    '        font-size: 11px;\n'
    '        font-weight: 700;\n'
    '        color: #c084fc;\n'
    '      }'
)
NEW = (
    '.comment-card-op {\n'
    '        font-size: 11px;\n'
    '        font-weight: 700;\n'
    '        color: #0a0a0a;\n'
    '      }'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: OP badge → black')
else:
    errors.append('FAIL: .comment-card-op CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
