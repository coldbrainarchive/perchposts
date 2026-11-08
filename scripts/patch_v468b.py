#!/usr/bin/env python3
"""Patch v467 -> v468b:
Update .user-pill CSS to match search dropdown user pill styling:
- gap: 3px → 4px
- padding: 0 9px 0 6px → 0 7px (equal sides, matches search pills)
- font-size: 12px → 11px (matches search pills fontSize:11)
This makes all Xn pills (postcards, huddle page) look identical to
the user pills shown in the search dropdown.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v467.js'
dst = '_deploy/assets/index-DUcNPOLc-v468.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_CSS = ('display: inline-flex;\n        align-items: center;\n'
           '        gap: 3px;\n        height: 22px;\n'
           '        padding: 0 9px 0 6px;\n        border-radius: 999px;\n'
           '        border: 1px solid;\n        font-size: 12px;')
NEW_CSS = ('display: inline-flex;\n        align-items: center;\n'
           '        gap: 4px;\n        height: 22px;\n'
           '        padding: 0 7px;\n        border-radius: 999px;\n'
           '        border: 1px solid;\n        font-size: 11px;')

if OLD_CSS in content:
    content = content.replace(OLD_CSS, NEW_CSS, 1)
    print('OK: .user-pill CSS updated to match search pill styling')
else:
    errors.append('FAIL: .user-pill CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
