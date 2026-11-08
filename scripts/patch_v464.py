#!/usr/bin/env python3
"""Patch v463 -> v464:
1. Add fontSize:14 to all inline-flex pill badges (Xn + all sz=13 sites).
   Without explicit fontSize, Chrome renders emoji at the tiny inherited
   pill font-size (~11-12px) while Safari inflates them, causing mismatch.
2. Fix comment bubble bird: switch from display:inline-block to inline-flex
   with centering, remove display:block from emoji span. On Safari, display:block
   inside inline-block causes the emoji glyph to visually overflow the container
   and eat into the gap before the username.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v463.js'
dst = '_deploy/assets/index-DUcNPOLc-v464.js'

content = open(src, encoding='utf-8').read()
errors = []

BADGE_OLD = ('style:{position:`relative`,display:`inline-flex`,'
             'alignItems:`center`,justifyContent:`center`,'
             'width:16,height:16,verticalAlign:`middle`,flexShrink:0}')
BADGE_NEW = ('style:{position:`relative`,display:`inline-flex`,'
             'alignItems:`center`,justifyContent:`center`,'
             'fontSize:14,width:16,height:16,verticalAlign:`middle`,flexShrink:0}')

# ── 1. Xn badge (user-pill-badge) ─────────────────────────────────────────────
XN_OLD = 'className:`user-pill-badge`,' + BADGE_OLD
XN_NEW = 'className:`user-pill-badge`,' + BADGE_NEW
if XN_OLD in content:
    content = content.replace(XN_OLD, XN_NEW, 1)
    print('OK: Xn badge fontSize:14 added')
else:
    errors.append('FAIL: Xn badge not found')

# ── 2. All sz=13 pill badge sites (7 occurrences) ─────────────────────────────
n = content.count(BADGE_OLD)
if n == 7:
    content = content.replace(BADGE_OLD, BADGE_NEW)
    print(f'OK: sz=13 badge sites fontSize:14 added ({n} occurrences)')
elif n > 0:
    content = content.replace(BADGE_OLD, BADGE_NEW)
    print(f'OK: badge sites fontSize:14 added ({n} occurrences)')
else:
    errors.append('FAIL: sz=13 badge style not found')

# ── 3. Comment bubble: inline-block → inline-flex, remove display:block ────────
OLD_CMT = ('style:{position:`relative`,display:`inline-block`,'
           'fontSize:17,lineHeight:1,flexShrink:0,width:`17px`,height:`17px`},'
           'children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display:`block`},'
           'children:_bd&&_bd.e?_bd.e:`🐤`})')
NEW_CMT = ('style:{position:`relative`,display:`inline-flex`,'
           'alignItems:`center`,justifyContent:`center`,'
           'fontSize:17,lineHeight:1,flexShrink:0,width:`17px`,height:`17px`},'
           'children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``},'
           'children:_bd&&_bd.e?_bd.e:`🐤`})')
if OLD_CMT in content:
    content = content.replace(OLD_CMT, NEW_CMT, 1)
    print('OK: comment bubble bird switched to inline-flex, display:block removed')
else:
    errors.append('FAIL: comment bubble bird not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
