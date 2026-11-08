#!/usr/bin/env python3
"""Patch v369 -> v370: fix Invite button vertical alignment in huddle action row."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v369.js'
dst = '_deploy/assets/index-DUcNPOLc-v370.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsxs)(`span`,{style:{position:`relative`},children:['
NEW = '(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,alignItems:`center`},children:['

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Invite button wrapper aligned')
else:
    errors.append('FAIL: Invite span wrapper not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
