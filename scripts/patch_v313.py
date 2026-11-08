#!/usr/bin/env python3
"""Patch v312 -> v313: fix comments-shell sticky offset to appear BELOW the nav bar.
The app-topbar is sticky at top:0 with height ~73px (search-shell uses top:73px).
The comments section must stick at top:73px so it appears below the nav, not behind it.
Also set height:calc(100dvh - 73px) to fill remaining viewport."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v312.js'
dst = '_deploy/assets/index-DUcNPOLc-v313.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_SHELL = (
    '.comments-shell {\n'
    '        margin-top: 18px;\n'
    '        position: sticky;\n'
    '        top: 0;\n'
    '        height: 100dvh;\n'
    '        display: flex;\n'
    '        flex-direction: column;\n'
    '        overflow: hidden;\n'
    '      }'
)
NEW_SHELL = (
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
if OLD_SHELL in content:
    content = content.replace(OLD_SHELL, NEW_SHELL, 1)
    print('OK: comments-shell sticky offset corrected to top:73px (below nav bar)')
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
