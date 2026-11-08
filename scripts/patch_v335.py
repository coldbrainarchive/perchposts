#!/usr/bin/env python3
"""Patch v334 -> v335:
- Remove scroll-behavior:smooth from .chat-window (was preventing JS scrollTop from landing)
- Add padding-bottom:90px so action sheet is visible without scrolling when last comment is tapped
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v334.js'
dst = '_deploy/assets/index-DUcNPOLc-v335.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_WINDOW = (
    '.chat-window {\n'
    '        flex: 1;\n'
    '        min-height: 0;\n'
    '        overflow-y: auto;\n'
    '        display: flex;\n'
    '        flex-direction: column;\n'
    '        gap: 6px;\n'
    '        position: relative;\n'
    '        padding: 14px 12px;\n'
    '        scroll-behavior: smooth;\n'
    '      }'
)
NEW_WINDOW = (
    '.chat-window {\n'
    '        flex: 1;\n'
    '        min-height: 0;\n'
    '        overflow-y: auto;\n'
    '        display: flex;\n'
    '        flex-direction: column;\n'
    '        gap: 6px;\n'
    '        position: relative;\n'
    '        padding: 14px 12px 90px;\n'
    '      }'
)
if OLD_WINDOW in content:
    content = content.replace(OLD_WINDOW, NEW_WINDOW, 1)
    print('OK: removed scroll-behavior:smooth, added 90px bottom padding')
else:
    errors.append('FAIL: .chat-window CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
