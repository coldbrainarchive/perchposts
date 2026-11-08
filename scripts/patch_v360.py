#!/usr/bin/env python3
"""Patch v359 -> v360: HUDDLES pill in huddle new post header uses small size to match user pill."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v359.js'
dst = '_deploy/assets/index-DUcNPOLc-v360.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '(0,L.jsx)(Ar,{boardName:`Huddles`,small:!1})'
NEW = '(0,L.jsx)(Ar,{boardName:`Huddles`,small:!0})'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: HUDDLES pill changed to small size')
else:
    errors.append('FAIL: HUDDLES pill not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
