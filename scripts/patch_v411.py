#!/usr/bin/env python3
"""Patch v410 -> v411:
- Nav: switch from translateY to marginTop so content below also shifts down (no exposed gap)
- Spinner container: grows from 0 to 60px height with overflow:hidden — spinner reveals from top
- Spinner: positioned at bottom of container so it peeks in as container grows
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v410.js'
dst = '_deploy/assets/index-DUcNPOLc-v411.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Nav: marginTop instead of translateY ────────────────────────────────────
OLD_NAV = (
    'style:{transform:`translateY(${g*60}px)`,'
    'transition:y?`none`:`transform 0.05s ease-out`},children:['
)
NEW_NAV = (
    'style:{marginTop:`${g*60}px`,'
    'transition:y?`none`:`margin-top 0.15s ease-out`},children:['
)
if OLD_NAV in content:
    content = content.replace(OLD_NAV, NEW_NAV, 1)
    print('OK: nav uses marginTop — content below moves with it')
else:
    errors.append('FAIL: nav style not found')

# ── 2. Spinner container: grows from 0→60px, overflow hidden ──────────────────
OLD_CONTAINER = (
    'position:`fixed`,top:0,left:0,right:0,height:60,zIndex:9999,'
    'display:`flex`,alignItems:`center`,justifyContent:`center`,'
    'background:`#16171d`,pointerEvents:`none`}'
)
NEW_CONTAINER = (
    'position:`fixed`,top:0,left:0,right:0,'
    'height:`${y?60:g*60}px`,overflow:`hidden`,'
    'zIndex:9999,background:`#16171d`,pointerEvents:`none`}'
)
if OLD_CONTAINER in content:
    content = content.replace(OLD_CONTAINER, NEW_CONTAINER, 1)
    print('OK: spinner container grows with pull (overflow hidden)')
else:
    errors.append('FAIL: spinner container not found')

# ── 3. Spinner: anchor to bottom so it reveals from top ───────────────────────
OLD_SPINNER = (
    '{width:28,height:28,borderRadius:`50%`,border:`2.5px solid #c084fc`,'
    'borderTopColor:`transparent`,'
    'opacity:y?1:Math.min(g*1.4,1),'
    'transform:`scale(${y?1:0.5+g*0.5}) rotate(${y?0:g*270}deg)`,'
    'animation:y?`ptr-spin 0.6s linear infinite`:`none`,'
    'transition:y?`none`:`transform 0.05s ease-out,opacity 0.05s`}'
)
NEW_SPINNER = (
    '{position:`absolute`,bottom:12,left:`50%`,'
    'transform:`translateX(-50%) scale(${y?1:0.5+g*0.5}) rotate(${y?0:g*270}deg)`,'
    'width:26,height:26,borderRadius:`50%`,'
    'border:`2.5px solid #c084fc`,borderTopColor:`transparent`,'
    'opacity:y?1:Math.min(g*1.6,1),'
    'animation:y?`ptr-spin 0.6s linear infinite`:`none`,'
    'transition:y?`none`:`transform 0.05s ease-out,opacity 0.05s`}'
)
if OLD_SPINNER in content:
    content = content.replace(OLD_SPINNER, NEW_SPINNER, 1)
    print('OK: spinner anchored to bottom of container')
else:
    errors.append('FAIL: spinner inner style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
