#!/usr/bin/env python3
"""Patch v139 -> v140: dark/earthy bird variants + constrain spots to face area."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v139.js'
dst = '_deploy/assets/index-DUcNPOLc-v140.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Update filter: add dark/earthy variants (~25% of users) ───────────────
# Current: _sat=(_a>>5)%40+80,_bri=(_a>>8)%20+92
# New: if (_a>>14)%4===0 → dark/muted (sat 40-65%, bri 48-68%)
#      else → bright vivid (sat 80-120%, bri 92-112%)
OLD_SAT = (
    "_sat=(_a>>5)%40+80,_bri=(_a>>8)%20+92,"
    "_f=`hue-rotate(${_a%360}deg) saturate(${_sat}%) brightness(${_bri}%)`;"
)
NEW_SAT = (
    "_dk=(_a>>14)%4===0,"
    "_sat=_dk?((_a>>5)%25+40):((_a>>5)%40+80),"
    "_bri=_dk?((_a>>8)%20+48):((_a>>8)%20+92),"
    "_f=`hue-rotate(${_a%360}deg) saturate(${_sat}%) brightness(${_bri}%)`;"
)

if OLD_SAT in content:
    content = content.replace(OLD_SAT, NEW_SAT, 1)
    print('OK: dark/earthy variant added to filter')
else:
    errors.append('FAIL: filter sat/bri block not found')

# ── 2. Constrain spots to bird face area ─────────────────────────────────────
# Face area: x 10-50% (left-centre, avoids beak on right), y 5-42% (upper head)
# Spot size: 12-20% of emoji size — visible but not huge
OLD_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%5*0.1+0.18,y:(sv>>6)%4*0.1+0.3,w:(sv>>9)%2*0.08+0.18});}'
    'return spots;}'
)
NEW_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    # x: 0.10–0.46 (left to centre — avoids beak on right)
    # y: 0.05–0.38 (upper face/head only)
    # w: 0.12–0.19 (small spot)
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%5*0.09+0.10,y:(sv>>6)%4*0.08+0.05,w:(sv>>9)%2*0.07+0.12});}'
    'return spots;}'
)

if OLD_SPOTS in content:
    content = content.replace(OLD_SPOTS, NEW_SPOTS, 1)
    print('OK: spots constrained to face area')
else:
    errors.append('FAIL: _mkSpots block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
