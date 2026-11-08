#!/usr/bin/env python3
"""Patch v567 -> v568:
- + SVG: add display:block to remove inline baseline offset; rebalance coordinates in clean 12x12 space
- PostAttachment video: autoPlay+muted+loop+playsInline so iOS shows frames (GIF-style silent autoplay)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v567.js'
dst = '_deploy/assets/index-DUcNPOLc-v568.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append(f'FAIL ({label}): not found')
    elif n > 1:
        errors.append(f'FAIL ({label}): {n} matches (not unique)')
    else:
        content = content.replace(old, new)
        print(f'OK: {label}')

# ── 1. Center + SVG: display:block + symmetric 12x12 coords ──
patch(
    '(0,L.jsx)(`svg`,{width:11,height:11,viewBox:`0 0 14 14`,stroke:`currentColor`,strokeWidth:1.8,strokeLinecap:`round`,fill:`none`,children:(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`line`,{x1:7,y1:1,x2:7,y2:13}),(0,L.jsx)(`line`,{x1:1,y1:7,x2:13,y2:7})]})})',
    '(0,L.jsx)(`svg`,{width:12,height:12,viewBox:`0 0 12 12`,stroke:`currentColor`,strokeWidth:1.8,strokeLinecap:`round`,fill:`none`,style:{display:`block`},children:(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`line`,{x1:6,y1:1.5,x2:6,y2:10.5}),(0,L.jsx)(`line`,{x1:1.5,y1:6,x2:10.5,y2:6})]})})',
    'center + SVG with display:block and symmetric coords'
)

# ── 2. PostAttachment video: autoPlay+muted+loop+playsInline for iOS frame display ──
patch(
    '(0,L.jsx)(`video`,{src:n,controls:!0,preload:`metadata`,playsInline:!0,style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}})',
    '(0,L.jsx)(`video`,{src:n,controls:!0,autoPlay:!0,muted:!0,loop:!0,playsInline:!0,preload:`auto`,style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}})',
    'video autoPlay muted loop playsInline for iOS thumbnails'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print(f'Paren delta: {p_delta}, Brace delta: {b_delta}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
