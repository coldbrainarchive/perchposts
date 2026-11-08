#!/usr/bin/env python3
"""Patch v143 -> v144: shift spots to right-of-eye / cheek area."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v143.js'
dst = '_deploy/assets/index-DUcNPOLc-v144.js'

content = open(src, encoding='utf-8').read()
errors = []

# Eye sits ~30-40% from left. Right-of-eye cheek: x 0.38-0.56, y 0.30-0.48.
# x: (sv>>3)%4*0.06+0.38  → 0.38 / 0.44 / 0.50 / 0.56
# y: (sv>>6)%4*0.06+0.30  → 0.30 / 0.36 / 0.42 / 0.48
OLD_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%4*0.07+0.18,y:(sv>>6)%4*0.07+0.28,w:(sv>>9)%2*0.05+0.12});}'
    'return spots;}'
)
NEW_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%4*0.06+0.38,y:(sv>>6)%4*0.06+0.30,w:(sv>>9)%2*0.05+0.12});}'
    'return spots;}'
)

if OLD_SPOTS in content:
    content = content.replace(OLD_SPOTS, NEW_SPOTS, 1)
    print('OK: spots moved to right-of-eye cheek area')
else:
    errors.append('FAIL: _mkSpots block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
