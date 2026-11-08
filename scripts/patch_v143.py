#!/usr/bin/env python3
"""Patch v142 -> v143: fix spots containment + nail face coordinates."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v142.js'
dst = '_deploy/assets/index-DUcNPOLc-v143.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Fix signup bird: nest inside position:relative box with explicit size ──
# Problem: outer span is position:absolute with no explicit dimensions, so the
# absolutely-positioned spot children escape to a parent container.
# Fix: outer span keeps position:absolute for layout; inner span is
# position:relative with explicit 40x40 box so spots are truly contained.
OLD_SIGNUP = (
    'var _sp=_mkSpots(_a);'
    'return(0,L.jsxs)(`span`,{style:{position:`absolute`,left:12,fontSize:40,'
    'lineHeight:1,display:`inline-block`},'
    'children:['
    '(0,L.jsx)(`span`,{style:{filter:_f},children:_e}),'
    '..._spEls(_sp,40)'
    ']})'
)
NEW_SIGNUP = (
    'var _sp=_mkSpots(_a);'
    'return(0,L.jsx)(`span`,{style:{position:`absolute`,left:12},'
    'children:(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,'
    'width:`40px`,height:`40px`,fontSize:`40px`,lineHeight:1},'
    'children:['
    '(0,L.jsx)(`span`,{style:{filter:_f},children:_e}),'
    '..._spEls(_sp,40)'
    ']})})'
)

if OLD_SIGNUP in content:
    content = content.replace(OLD_SIGNUP, NEW_SIGNUP, 1)
    print('OK: signup bird wrapped in explicit 40x40 relative container')
else:
    errors.append('FAIL: signup bird block not found')

# ── 2. Fix badge: add explicit size so spots don't escape ─────────────────────
OLD_BADGE = (
    'i&&(0,L.jsxs)(`span`,{className:`user-pill-badge`,'
    'style:{position:`relative`,display:`inline-block`},'
    'children:['
    '(0,L.jsx)(`span`,{style:typeof i===`object`&&i.f?{filter:i.f}:{},'
    'children:typeof i===`object`&&i.e?i.e:i}),'
    '...(typeof i===`object`&&i.s?_spEls(i.s,14):[])'
    ']})'
)
NEW_BADGE = (
    'i&&(0,L.jsxs)(`span`,{className:`user-pill-badge`,'
    'style:{position:`relative`,display:`inline-block`,width:`1.1em`,height:`1.1em`,'
    'lineHeight:1,verticalAlign:`middle`},'
    'children:['
    '(0,L.jsx)(`span`,{style:typeof i===`object`&&i.f?{filter:i.f}:{},'
    'children:typeof i===`object`&&i.e?i.e:i}),'
    '...(typeof i===`object`&&i.s?_spEls(i.s,14):[])'
    ']})'
)

if OLD_BADGE in content:
    content = content.replace(OLD_BADGE, NEW_BADGE, 1)
    print('OK: badge wrapped in explicit 1.1em relative container')
else:
    errors.append('FAIL: badge block not found')

# ── 3. Update spot coordinates to land on the face ───────────────────────────
# Bird emoji face occupies roughly the centre of the glyph.
# Left cheek / behind-eye target: x 0.18–0.40, y 0.28–0.50
# x: (sv>>3)%4*0.07+0.18  → 0.18, 0.25, 0.32, 0.39
# y: (sv>>6)%4*0.07+0.28  → 0.28, 0.35, 0.42, 0.49
OLD_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%4*0.08+0.25,y:(sv>>6)%4*0.07+0.18,w:(sv>>9)%2*0.05+0.12});}'
    'return spots;}'
)
NEW_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%4*0.07+0.18,y:(sv>>6)%4*0.07+0.28,w:(sv>>9)%2*0.05+0.12});}'
    'return spots;}'
)

if OLD_SPOTS in content:
    content = content.replace(OLD_SPOTS, NEW_SPOTS, 1)
    print('OK: spot coordinates updated to face area')
else:
    errors.append('FAIL: _mkSpots block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
