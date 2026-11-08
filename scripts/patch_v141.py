#!/usr/bin/env python3
"""Patch v140 -> v141: move spots to back-left of bird head (behind the eye)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v140.js'
dst = '_deploy/assets/index-DUcNPOLc-v141.js'

content = open(src, encoding='utf-8').read()
errors = []

# Bird emoji head sits roughly in the middle of the bounding box.
# Eye is ~35-45% from left. "Back of head" / behind-eye is the left side: x 4-24%.
# Vertically the head proper sits around 22-48% down the box.
# x: (sv>>3)%4*0.06+0.04  → 0.04 / 0.10 / 0.16 / 0.22  (back-left of head)
# y: (sv>>6)%4*0.07+0.22  → 0.22 / 0.29 / 0.36 / 0.43  (head height band)
# w: (sv>>9)%2*0.05+0.12  → 0.12 or 0.17               (small spots)

OLD_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%5*0.09+0.10,y:(sv>>6)%4*0.08+0.05,w:(sv>>9)%2*0.07+0.12});}'
    'return spots;}'
)
NEW_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%4*0.06+0.04,y:(sv>>6)%4*0.07+0.22,w:(sv>>9)%2*0.05+0.12});}'
    'return spots;}'
)

if OLD_SPOTS in content:
    content = content.replace(OLD_SPOTS, NEW_SPOTS, 1)
    print('OK: spots moved to back-left of head')
else:
    errors.append('FAIL: _mkSpots block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
