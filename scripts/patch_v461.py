#!/usr/bin/env python3
"""Patch v460 -> v461:
Revert the Xn badge container from inline-block/14px back to the original
inline-flex/16px. The explicit fontSize:14 caused the emoji glyph to overflow
the 14px container and overlap the username text. With inline-flex+centering
the emoji renders at the pill's inherited 12px and sits centered in a 16px
reference box — spots at % positions correctly target the bird glyph.
Keep display:block on the emoji span (no regression).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v460.js'
dst = '_deploy/assets/index-DUcNPOLc-v461.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── Revert badge container to inline-flex 16×16 ───────────────────────────────
OLD_BADGE = ('className:`user-pill-badge`,style:{position:`relative`,'
             'display:`inline-block`,fontSize:14,lineHeight:1,'
             'width:`14px`,height:`14px`,verticalAlign:`middle`,flexShrink:0}')
NEW_BADGE = ('className:`user-pill-badge`,style:{position:`relative`,'
             'display:`inline-flex`,alignItems:`center`,justifyContent:`center`,'
             'width:16,height:16,verticalAlign:`middle`,flexShrink:0}')
if OLD_BADGE in content:
    content = content.replace(OLD_BADGE, NEW_BADGE, 1)
    print('OK: badge reverted to inline-flex 16x16')
else:
    errors.append('FAIL: badge not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
