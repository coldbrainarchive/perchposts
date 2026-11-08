#!/usr/bin/env python3
"""Patch v141 -> v142: shift spots right onto the actual face (left cheek area)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v141.js'
dst = '_deploy/assets/index-DUcNPOLc-v142.js'

content = open(src, encoding='utf-8').read()
errors = []

# Bird face is centred in the emoji box, not at the far left edge.
# x: 0.25–0.49 puts dots on the left cheek/side of face (behind the eye)
# y: 0.18–0.39 keeps them in the upper-face / forehead band
OLD_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%4*0.06+0.04,y:(sv>>6)%4*0.07+0.22,w:(sv>>9)%2*0.05+0.12});}'
    'return spots;}'
)
NEW_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%4*0.08+0.25,y:(sv>>6)%4*0.07+0.18,w:(sv>>9)%2*0.05+0.12});}'
    'return spots;}'
)

if OLD_SPOTS in content:
    content = content.replace(OLD_SPOTS, NEW_SPOTS, 1)
    print('OK: spots shifted onto face (left cheek)')
else:
    errors.append('FAIL: _mkSpots block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
