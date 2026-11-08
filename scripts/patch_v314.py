#!/usr/bin/env python3
"""Patch v313 -> v314: add card/bubble styling to comments-shell container.
The sticky container is working but has no visible card — add background,
border, and border-radius to match the reference screenshot."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v313.js'
dst = '_deploy/assets/index-DUcNPOLc-v314.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_SHELL = (
    '.comments-shell {\n'
    '        margin-top: 0;\n'
    '        position: sticky;\n'
    '        top: 73px;\n'
    '        height: calc(100dvh - 73px);\n'
    '        display: flex;\n'
    '        flex-direction: column;\n'
    '        overflow: hidden;\n'
    '        z-index: 15;\n'
    '      }'
)
NEW_SHELL = (
    '.comments-shell {\n'
    '        margin-top: 18px;\n'
    '        position: sticky;\n'
    '        top: 73px;\n'
    '        height: calc(100dvh - 91px);\n'
    '        display: flex;\n'
    '        flex-direction: column;\n'
    '        overflow: hidden;\n'
    '        z-index: 15;\n'
    '        background: linear-gradient(180deg, #1b1d24 0%, #14161c 100%);\n'
    '        border: 1px solid #2e303a;\n'
    '        border-radius: 18px;\n'
    '        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.2);\n'
    '      }'
)
if OLD_SHELL in content:
    content = content.replace(OLD_SHELL, NEW_SHELL, 1)
    print('OK: card/bubble styling added to comments-shell')
else:
    errors.append('FAIL: comments-shell CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
