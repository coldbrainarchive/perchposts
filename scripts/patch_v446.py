#!/usr/bin/env python3
"""Patch v445 -> v446:
Move CSS filter onto the emoji span only (not the container),
so spots keep their own colours instead of being hue-rotated with the bird.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v445.js'
dst = '_deploy/assets/index-DUcNPOLc-v446.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = ('(0,L.jsxs)(`span`,{style:{filter:_jd.f||``,position:`relative`,display:`inline-block`,lineHeight:1},'
       'children:[_jd.e||`🐦`,...(_jd.s?_spEls(_jd.s,13):[])]})')
NEW = ('(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,lineHeight:1},'
       'children:[(0,L.jsx)(`span`,{style:{filter:_jd.f||``,display:`block`},children:_jd.e||`🐦`}),'
       '...(_jd.s?_spEls(_jd.s,13):[])]})')

count = content.count(OLD)
if count > 0:
    content = content.replace(OLD, NEW)
    print(f'OK: filter moved onto emoji span only ({count} occurrences fixed)')
else:
    errors.append('FAIL: bird container pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
