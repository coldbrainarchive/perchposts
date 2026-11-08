#!/usr/bin/env python3
"""Patch v407 -> v408:
- Pull-to-refresh: longer pull distance (100px instead of 72px)
- Instagram-style: spinner slides in from top as you pull, scales up
- Haptic feedback (vibrate 12ms) when threshold is reached
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v407.js'
dst = '_deploy/assets/index-DUcNPOLc-v408.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Longer pull distance: 72 → 110 ────────────────────────────────────────
OLD_DIST = 'x.current.pullY=Math.min(n/72,1)'
NEW_DIST = 'x.current.pullY=Math.min(n/110,1)'
if OLD_DIST in content:
    content = content.replace(OLD_DIST, NEW_DIST, 1)
    print('OK: pull distance increased to 110px')
else:
    errors.append('FAIL: pull divisor not found')

# ── 2. Haptics when threshold reached ────────────────────────────────────────
OLD_ACTIVE = 'x.current.active=!0;requestAnimationFrame(()=>v(x.current.pullY||0));return'
NEW_ACTIVE = (
    'x.current.active=!0;'
    'if(x.current.pullY>=1&&!x.current.hapticFired){'
    'x.current.hapticFired=!0;'
    'try{navigator.vibrate&&navigator.vibrate(12);}catch(_){}'
    '}'
    'if(x.current.pullY<0.95)x.current.hapticFired=!1;'
    'requestAnimationFrame(()=>v(x.current.pullY||0));return'
)
if OLD_ACTIVE in content:
    content = content.replace(OLD_ACTIVE, NEW_ACTIVE, 1)
    print('OK: haptic feedback added at threshold')
else:
    errors.append('FAIL: active set not found')

# ── 3. Instagram-style indicator: slides in from top, scales with pull ────────
# Container: translateY moves from -56px (hidden above) to 0 (visible) as g goes 0→1
# Spinner: scales from 0.4 to 1 and fades in
OLD_CONTAINER = (
    '{style:{position:`fixed`,top:0,left:0,right:0,height:56,zIndex:9999,'
    'display:`flex`,alignItems:`center`,justifyContent:`center`,pointerEvents:`none`},'
    'children:(0,L.jsx)(`div`,{style:{width:20,height:20,borderRadius:`50%`,'
    'border:`2.5px solid #c084fc`,borderTopColor:`transparent`,'
    'opacity:y?1:g,transform:`rotate(${y?0:g*270}deg)`,'
    'animation:y?`ptr-spin 0.6s linear infinite`:`none`,'
    'transition:y?`none`:`opacity 0.1s`}})}'
)
NEW_CONTAINER = (
    '{style:{position:`fixed`,top:0,left:0,right:0,height:60,zIndex:9999,'
    'display:`flex`,alignItems:`flex-end`,justifyContent:`center`,'
    'paddingBottom:10,pointerEvents:`none`,'
    'transform:`translateY(${y?0:(g-1)*60}px)`,'
    'transition:y?`none`:`transform 0.05s ease-out`},'
    'children:(0,L.jsx)(`div`,{style:{width:28,height:28,borderRadius:`50%`,'
    'border:`2.5px solid #c084fc`,borderTopColor:`transparent`,'
    'opacity:y?1:Math.min(g*1.4,1),'
    'transform:`scale(${y?1:0.5+g*0.5}) rotate(${y?0:g*270}deg)`,'
    'animation:y?`ptr-spin 0.6s linear infinite`:`none`,'
    'transition:y?`none`:`transform 0.05s ease-out,opacity 0.05s`}})}'
)
if OLD_CONTAINER in content:
    content = content.replace(OLD_CONTAINER, NEW_CONTAINER, 1)
    print('OK: Instagram-style indicator added')
else:
    errors.append('FAIL: spinner container not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
