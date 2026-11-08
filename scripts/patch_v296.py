#!/usr/bin/env python3
"""Patch v295 -> v296: fix bird spots leaking to top-left of screen.
The user-pill-badge span had display:inline-flex but no position:relative,
so position:absolute spots escaped to the nearest positioned ancestor on the page.
Fix: add position:relative to the badge container."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v295.js'
dst = '_deploy/assets/index-DUcNPOLc-v296.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'user-pill-badge`,style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,width:16,height:16,verticalAlign:`middle`,flexShrink:0}'
)
NEW = (
    'user-pill-badge`,style:{position:`relative`,display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,width:16,height:16,verticalAlign:`middle`,flexShrink:0}'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: position:relative added to user-pill-badge — spots anchored correctly')
else:
    errors.append('FAIL: user-pill-badge style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
