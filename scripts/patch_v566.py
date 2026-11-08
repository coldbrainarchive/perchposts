#!/usr/bin/env python3
"""Patch v565 -> v566:
- + button: replace text + with inline SVG rounded-cap cross (lighter, matches arrow aesthetic)
- PostAttachment images: tap opens full-screen lightbox overlay (DOM-based, no React state needed)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v565.js'
dst = '_deploy/assets/index-DUcNPOLc-v566.js'

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

# ── 1. Replace text + with rounded SVG cross matching send button weight ──
patch(
    '(0,L.jsx)(`span`,{style:{lineHeight:1,display:`block`,marginTop:-2},children:`+`})',
    '(0,L.jsx)(`svg`,{width:14,height:14,viewBox:`0 0 14 14`,stroke:`currentColor`,strokeWidth:2,strokeLinecap:`round`,fill:`none`,children:(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`line`,{x1:7,y1:1,x2:7,y2:13}),(0,L.jsx)(`line`,{x1:1,y1:7,x2:13,y2:7})]})})',
    'replace + text with rounded SVG cross'
)

# ── 2. PostAttachment image: add tap-to-fullscreen lightbox ──
patch(
    '(0,L.jsx)(`img`,{src:n,alt:``,style:{maxWidth:`100%`,borderRadius:10,display:`block`,maxHeight:400,objectFit:`cover`},onError:e=>{e.target.style.display=`none`}})',
    '(0,L.jsx)(`img`,{src:n,alt:``,style:{maxWidth:`100%`,borderRadius:10,display:`block`,maxHeight:400,objectFit:`cover`,cursor:`zoom-in`},onError:e=>{e.target.style.display=`none`},onClick:()=>{let _ov=document.createElement(`div`);_ov.style.cssText=`position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:zoom-out`;let _im=document.createElement(`img`);_im.src=n;_im.style.cssText=`max-width:92vw;max-height:92vh;border-radius:10px;object-fit:contain`;_ov.appendChild(_im);_ov.onclick=()=>document.body.removeChild(_ov);document.body.appendChild(_ov)}})',
    'image tap opens fullscreen lightbox'
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
