#!/usr/bin/env python3
"""Patch v411 -> v412:
- Spinner: fix right-offset by using flex centering instead of position:absolute + left:50%
- Background: match nav exactly (rgba(11,15,18,0.92))
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v411.js'
dst = '_deploy/assets/index-DUcNPOLc-v412.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Container: flex centering + matching nav background ────────────────────
OLD_CONTAINER = (
    'position:`fixed`,top:0,left:0,right:0,'
    'height:`${y?60:g*60}px`,overflow:`hidden`,'
    'zIndex:9999,background:`#16171d`,pointerEvents:`none`}'
)
NEW_CONTAINER = (
    'position:`fixed`,top:0,left:0,right:0,'
    'height:`${y?60:g*60}px`,overflow:`hidden`,'
    'display:`flex`,justifyContent:`center`,alignItems:`flex-end`,paddingBottom:10,'
    'zIndex:9999,background:`rgba(11,15,18,0.95)`,pointerEvents:`none`}'
)
if OLD_CONTAINER in content:
    content = content.replace(OLD_CONTAINER, NEW_CONTAINER, 1)
    print('OK: container uses flex centering + matching nav bg')
else:
    errors.append('FAIL: container style not found')

# ── 2. Spinner: remove absolute positioning, let flex centre it ───────────────
OLD_SPINNER = (
    '{position:`absolute`,bottom:12,left:`50%`,'
    'transform:`translateX(-50%) scale(${y?1:0.5+g*0.5}) rotate(${y?0:g*270}deg)`,'
    'width:26,height:26,borderRadius:`50%`,'
    'border:`2.5px solid #c084fc`,borderTopColor:`transparent`,'
    'opacity:y?1:Math.min(g*1.6,1),'
    'animation:y?`ptr-spin 0.6s linear infinite`:`none`,'
    'transition:y?`none`:`transform 0.05s ease-out,opacity 0.05s`}'
)
NEW_SPINNER = (
    '{width:26,height:26,borderRadius:`50%`,'
    'border:`2.5px solid #c084fc`,borderTopColor:`transparent`,'
    'opacity:y?1:Math.min(g*1.6,1),'
    'transform:`scale(${y?1:0.5+g*0.5}) rotate(${y?0:g*270}deg)`,'
    'animation:y?`ptr-spin 0.6s linear infinite`:`none`,'
    'transition:y?`none`:`transform 0.05s ease-out,opacity 0.05s`}'
)
if OLD_SPINNER in content:
    content = content.replace(OLD_SPINNER, NEW_SPINNER, 1)
    print('OK: spinner centred via flex parent, no position:absolute')
else:
    errors.append('FAIL: spinner style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
