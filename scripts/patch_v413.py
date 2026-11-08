#!/usr/bin/env python3
"""Patch v412 -> v413:
- Nav: add paddingTop=safe-area-inset-top so nav bg fills status bar gap (always black)
- Nav: remove transition so it stays perfectly in sync with spinner container
- Container: match exact same background, extend paddingTop for safe area
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v412.js'
dst = '_deploy/assets/index-DUcNPOLc-v413.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Nav: no transition + safe area padding so header always looks solid black
OLD_NAV = (
    'style:{marginTop:`${g*60}px`,'
    'transition:y?`none`:`margin-top 0.15s ease-out`},children:['
)
NEW_NAV = (
    'style:{marginTop:`${g*60}px`},children:['
)
if OLD_NAV in content:
    content = content.replace(OLD_NAV, NEW_NAV, 1)
    print('OK: nav margin-top in sync (no transition lag)')
else:
    errors.append('FAIL: nav style not found')

# ── 2. Spinner container: extend into safe area, always show dark bg ───────────
OLD_CONTAINER = (
    'position:`fixed`,top:0,left:0,right:0,'
    'height:`${y?60:g*60}px`,overflow:`hidden`,'
    'display:`flex`,justifyContent:`center`,alignItems:`flex-end`,paddingBottom:10,'
    'zIndex:9999,background:`rgba(11,15,18,0.95)`,pointerEvents:`none`}'
)
NEW_CONTAINER = (
    'position:`fixed`,top:0,left:0,right:0,'
    'height:`calc(${y?60:g*60}px + env(safe-area-inset-top))`,'
    'overflow:`hidden`,'
    'display:`flex`,justifyContent:`center`,alignItems:`flex-end`,paddingBottom:10,'
    'zIndex:9999,background:`rgba(11,15,18,0.98)`,pointerEvents:`none`}'
)
if OLD_CONTAINER in content:
    content = content.replace(OLD_CONTAINER, NEW_CONTAINER, 1)
    print('OK: spinner container extends into safe area with solid dark bg')
else:
    errors.append('FAIL: spinner container not found')

# ── 3. Always show at least the safe-area strip (even at g=0) ──────────────────
# Also ensure the (g>0||y) condition shows a baseline strip
OLD_COND = '(g>0||y)&&(0,L.jsx)(`div`,{style:{'
NEW_COND = '(0,L.jsx)(`div`,{style:{'
if OLD_COND in content:
    content = content.replace(OLD_COND, NEW_COND, 1)
    print('OK: spinner container always visible (safe area strip at rest)')
else:
    errors.append('FAIL: spinner condition not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
