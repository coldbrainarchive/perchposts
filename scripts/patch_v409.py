#!/usr/bin/env python3
"""Patch v408 -> v409:
- Spinner moved from fixed overlay to absolute above nav (no overlap)
- Nav slides DOWN with transform as you pull, creating space above it
- Spinner appears in the revealed space above the nav
- Haptics note: navigator.vibrate works on Android; iOS doesn't support Vibration API
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v408.js'
dst = '_deploy/assets/index-DUcNPOLc-v409.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Change spinner from fixed overlay → sits above nav in the revealed space
# The spinner container: change from position:fixed to an absolute block
# that only shows when pull is active, positioned right before the nav
OLD_SPINNER_CONTAINER = (
    '(g>0||y)&&(0,L.jsx)(`div`,{style:{position:`fixed`,top:0,left:0,right:0,height:60,zIndex:9999,'
    'display:`flex`,alignItems:`flex-end`,justifyContent:`center`,'
    'paddingBottom:10,pointerEvents:`none`,'
    'transform:`translateY(${y?0:(g-1)*60}px)`,'
    'transition:y?`none`:`transform 0.05s ease-out`},'
)
NEW_SPINNER_CONTAINER = (
    '(g>0||y)&&(0,L.jsx)(`div`,{style:{position:`fixed`,top:0,left:0,right:0,height:60,zIndex:9999,'
    'display:`flex`,alignItems:`center`,justifyContent:`center`,'
    'paddingTop:12,pointerEvents:`none`},'
)
if OLD_SPINNER_CONTAINER in content:
    content = content.replace(OLD_SPINNER_CONTAINER, NEW_SPINNER_CONTAINER, 1)
    print('OK: spinner repositioned to fixed top center')
else:
    errors.append('FAIL: spinner container not found')

# ── 2. Nav slides down with transform, content reveals spinner above ──────────
OLD_NAV = '(0,L.jsxs)(`nav`,{className:`app-topbar`,children:['
NEW_NAV = (
    '(0,L.jsxs)(`nav`,{className:`app-topbar`,'
    'style:{transform:`translateY(${g*60}px)`,transition:y?`none`:`transform 0.05s ease-out`},'
    'children:['
)
if OLD_NAV in content:
    content = content.replace(OLD_NAV, NEW_NAV, 1)
    print('OK: nav slides down on pull revealing spinner above')
else:
    errors.append('FAIL: nav not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
