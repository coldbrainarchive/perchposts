#!/usr/bin/env python3
"""Patch v566 -> v567:
- Lightbox: lock body scroll while open, restore on close
- PostAttachment video: add preload=metadata + playsInline so first frame shows on mobile
- + button: shrink SVG cross from 14->11px and strokeWidth 2->1.5 to match arrow visual weight
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v566.js'
dst = '_deploy/assets/index-DUcNPOLc-v567.js'

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

# ── 1. Lightbox: lock scroll on open, restore on close ──
patch(
    '_ov.onclick=()=>document.body.removeChild(_ov);document.body.appendChild(_ov',
    '_ov.onclick=()=>{document.body.removeChild(_ov);document.body.style.overflow=``};document.body.style.overflow=`hidden`;document.body.appendChild(_ov',
    'lightbox locks body scroll'
)

# ── 2. PostAttachment video: add preload + playsInline for mobile first frame ──
patch(
    '(0,L.jsx)(`video`,{src:n,controls:!0,style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}})',
    '(0,L.jsx)(`video`,{src:n,controls:!0,preload:`metadata`,playsInline:!0,style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}})',
    'PostAttachment video preload + playsInline'
)

# ── 3. Shrink + SVG: 14->11px viewBox, strokeWidth 2->1.5 ──
patch(
    '(0,L.jsx)(`svg`,{width:14,height:14,viewBox:`0 0 14 14`,stroke:`currentColor`,strokeWidth:2,strokeLinecap:`round`,fill:`none`,children:(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`line`,{x1:7,y1:1,x2:7,y2:13}),(0,L.jsx)(`line`,{x1:1,y1:7,x2:13,y2:7})]})})',
    '(0,L.jsx)(`svg`,{width:11,height:11,viewBox:`0 0 14 14`,stroke:`currentColor`,strokeWidth:1.8,strokeLinecap:`round`,fill:`none`,children:(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`line`,{x1:7,y1:1,x2:7,y2:13}),(0,L.jsx)(`line`,{x1:1,y1:7,x2:13,y2:7})]})})',
    'shrink + SVG to match arrow size'
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
