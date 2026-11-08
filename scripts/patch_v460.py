#!/usr/bin/env python3
"""Patch v459 -> v460:
Unify the bird badge in Xn (the canonical pill component used on postcards/feed)
to use the same structure as the search chip badge (position:relative,
display:inline-block, explicit fontSize+width+height, display:block on emoji span).
Previously Xn used inline-flex centering which offset spots differently.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v459.js'
dst = '_deploy/assets/index-DUcNPOLc-v460.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Fix Xn badge container: inline-flex+centering → inline-block+explicit size
OLD_BADGE = ('className:`user-pill-badge`,style:{position:`relative`,'
             'display:`inline-flex`,alignItems:`center`,justifyContent:`center`,'
             'width:16,height:16,verticalAlign:`middle`,flexShrink:0}')
NEW_BADGE = ('className:`user-pill-badge`,style:{position:`relative`,'
             'display:`inline-block`,fontSize:14,lineHeight:1,'
             'width:`14px`,height:`14px`,verticalAlign:`middle`,flexShrink:0}')
if OLD_BADGE in content:
    content = content.replace(OLD_BADGE, NEW_BADGE, 1)
    print('OK: Xn badge container changed to inline-block with explicit size')
else:
    errors.append('FAIL: Xn badge container not found')

# ── 2. Fix emoji span inside Xn badge: add display:block, always apply filter
OLD_EMJ = ('(0,L.jsx)(`span`,{style:typeof i===`object`&&i.f?{filter:i.f}:{},'
           'children:typeof i===`object`&&i.e?i.e:i})')
NEW_EMJ = ('(0,L.jsx)(`span`,{style:{filter:typeof i===`object`&&i.f?i.f:``,display:`block`},'
           'children:typeof i===`object`&&i.e?i.e:i})')
if OLD_EMJ in content:
    content = content.replace(OLD_EMJ, NEW_EMJ, 1)
    print('OK: Xn emoji span gets display:block + unconditional filter')
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
