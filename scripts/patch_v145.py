#!/usr/bin/env python3
"""Patch v144 -> v145: push spots right of eye + make them bigger blobby shapes."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v144.js'
dst = '_deploy/assets/index-DUcNPOLc-v145.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. _mkSpots: right-of-eye coords + blob shape data ───────────────────────
# Bird eye is roughly at x 50-60%. Right of eye / cheek: x 0.55-0.72
# y 0.32-0.50 keeps spots on the face proper.
# Add per-spot blob corner radii (r) and separate height (wh) for ellipses.
OLD_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    'spots.push({h:(sv*11+67)%360,x:(sv>>3)%4*0.06+0.38,y:(sv>>6)%4*0.06+0.30,w:(sv>>9)%2*0.05+0.12});}'
    'return spots;}'
)
NEW_SPOTS = (
    'function _mkSpots(a){'
    'if(a%10>=3)return null;'
    'var ns=(a%2)+1,spots=[];'
    'for(var si=0;si<ns;si++){'
    'var sv=a>>(si*7+5);'
    # x: 0.55–0.72 (right of eye, cheek zone)
    # y: 0.32–0.50 (face height)
    # w: 0.20–0.32 (bigger blobs)
    # wh: independent height ratio for ellipse look
    # r: seed for organic border-radius
    'spots.push({'
    'h:(sv*11+67)%360,'
    'x:(sv>>3)%3*0.085+0.55,'
    'y:(sv>>6)%4*0.06+0.32,'
    'w:(sv>>9)%3*0.06+0.20,'
    'wh:(sv>>12)%3*0.05+0.18,'
    'r:(sv>>15)%28+36'
    '});}'
    'return spots;}'
)

if OLD_SPOTS in content:
    content = content.replace(OLD_SPOTS, NEW_SPOTS, 1)
    print('OK: _mkSpots updated — right-of-eye coords + blob data')
else:
    errors.append('FAIL: _mkSpots block not found')

# ── 2. _spEls: use ellipse size + organic border-radius for blobby look ───────
OLD_SPELS = (
    "function _spEls(spots,sz){"
    "return(spots||[]).map(function(s,i){"
    "return(0,L.jsx)('span',{style:{position:'absolute',borderRadius:'50%',"
    "background:`hsl(${s.h},82%,62%)`,width:sz*s.w+'px',height:sz*s.w+'px',"
    "left:sz*s.x+'px',top:sz*s.y+'px',pointerEvents:'none',opacity:0.8,zIndex:1}},i);});}"
)
NEW_SPELS = (
    "function _spEls(spots,sz){"
    "return(spots||[]).map(function(s,i){"
    # Organic blob: four different corner radii derived from r seed
    "var r1=s.r,r2=100-s.r+8,r3=s.r+10,r4=100-s.r;"
    "return(0,L.jsx)('span',{style:{position:'absolute',"
    "borderRadius:`${r1}% ${r2}% ${r3}% ${r4}%`,"
    "background:`hsl(${s.h},85%,60%)`,"
    "width:sz*s.w+'px',height:sz*(s.wh||s.w)+'px',"
    "left:sz*s.x+'px',top:sz*s.y+'px',"
    "pointerEvents:'none',opacity:0.82,zIndex:1}},i);});}"
)

if OLD_SPELS in content:
    content = content.replace(OLD_SPELS, NEW_SPELS, 1)
    print('OK: _spEls updated — blobby ellipses with organic border-radius')
else:
    errors.append('FAIL: _spEls block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
