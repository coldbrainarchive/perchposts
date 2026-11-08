#!/usr/bin/env python3
"""Patch v365 -> v366: huddle postcards say 'View Huddle' instead of 'View Post'."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v365.js'
dst = '_deploy/assets/index-DUcNPOLc-v366.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD1 = 'children:`View Post →`'
NEW1 = 'children:e.is_huddle?`View Huddle →`:`View Post →`'
if OLD1 in content:
    content = content.replace(OLD1, NEW1, 1)
    print('OK: "View Post →" updated')
else:
    errors.append('FAIL: "View Post →" not found')

OLD2 = 'children:`View Post`'
NEW2 = 'children:e.is_huddle?`View Huddle`:`View Post`'
if OLD2 in content:
    content = content.replace(OLD2, NEW2, 1)
    print('OK: "View Post" button updated')
else:
    errors.append('FAIL: "View Post" button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
