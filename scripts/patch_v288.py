#!/usr/bin/env python3
"""Patch v287 -> v288: center hat bird in user-pill-badge by switching container
to inline-flex with align/justify center when rendering the hat bird image."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v287.js'
dst = '_deploy/assets/index-DUcNPOLc-v288.js'

content = open(src, encoding='utf-8').read()
errors = []

# Replace the user-pill-badge container style so hat bird is centered.
# Change from position:relative inline-block (designed for absolutely-positioned bird)
# to inline-flex centering that works with the new block image.
OLD_BADGE = (
    'className:`user-pill-badge`,style:{position:`relative`,display:`inline-block`,'
    'width:`1.1em`,height:`1.1em`,lineHeight:1,verticalAlign:`middle`}'
)
NEW_BADGE = (
    'className:`user-pill-badge`,style:{display:`inline-flex`,alignItems:`center`,'
    'justifyContent:`center`,width:16,height:16,verticalAlign:`middle`,flexShrink:0}'
)

if OLD_BADGE in content:
    content = content.replace(OLD_BADGE, NEW_BADGE, 1)
    print('OK: user-pill-badge uses inline-flex centering for hat bird')
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
