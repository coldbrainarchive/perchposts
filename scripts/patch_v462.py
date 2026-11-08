#!/usr/bin/env python3
"""Patch v461 -> v462:
Remove display:block from Xn's emoji span. In an inline-flex badge with
alignItems:center/justifyContent:center, display:block on the emoji flex item
causes it to expand differently than borbie's img tag, reducing the visual gap
between the bird and the username. Without display:block the emoji span sizes
to its content (same as before v460) and flex centering works correctly.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v461.js'
dst = '_deploy/assets/index-DUcNPOLc-v462.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = ('(0,L.jsx)(`span`,{style:{filter:typeof i===`object`&&i.f?i.f:``,display:`block`},'
       'children:typeof i===`object`&&i.e?i.e:i})')
NEW = ('(0,L.jsx)(`span`,{style:typeof i===`object`&&i.f?{filter:i.f}:{},'
       'children:typeof i===`object`&&i.e?i.e:i})')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: display:block removed from Xn emoji span')
else:
    errors.append('FAIL: Xn emoji span not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
