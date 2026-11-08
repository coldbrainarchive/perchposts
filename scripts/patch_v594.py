#!/usr/bin/env python3
"""Patch v593 -> v594:
1. Photo thumbnails: fixed 200px height with objectFit:cover (cropped preview like video poster)
2. Lightbox: swipe down >80px closes it
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v593.js'
dst = '_deploy/assets/index-DUcNPOLc-v594.js'

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

# ── 1. Photo thumbnail: fixed height cropped preview ──
# Change maxHeight:_mh to a fixed height:200 so it always shows as a compact thumbnail
patch(
    'style:{maxWidth:`100%`,borderRadius:10,display:`block`,maxHeight:_mh,objectFit:`cover`,cursor:`zoom-in`}',
    'style:{width:`100%`,borderRadius:10,display:`block`,height:_mh,objectFit:`cover`,cursor:`zoom-in`}',
    'photo thumbnail fixed height crop'
)

# ── 2. Lightbox: add swipe-down-to-close gesture ──
patch(
    'let _ov=document.createElement(`div`);_ov.style.cssText=`position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:zoom-out`;let _im=document.createElement(`img`);_im.src=n;_im.style.cssText=`max-width:92vw;max-height:92vh;border-radius:10px;object-fit:contain`;_ov.appendChild(_im);_ov.onclick=()=>{document.body.removeChild(_ov);document.body.style.overflow=``};document.body.style.overflow=`hidden`;document.body.appendChild(_ov)',
    'let _ov=document.createElement(`div`);_ov.style.cssText=`position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:zoom-out;transition:opacity 0.2s`;let _im=document.createElement(`img`);_im.src=n;_im.style.cssText=`max-width:92vw;max-height:92vh;border-radius:10px;object-fit:contain`;_ov.appendChild(_im);let _closeOv=()=>{document.body.removeChild(_ov);document.body.style.overflow=``};_ov.onclick=_closeOv;let _syOv=0;_ov.addEventListener(`touchstart`,_e=>{_syOv=_e.touches[0].clientY},{passive:!0});_ov.addEventListener(`touchend`,_e=>{if(_e.changedTouches[0].clientY-_syOv>80)_closeOv()},{passive:!0});document.body.style.overflow=`hidden`;document.body.appendChild(_ov)',
    'lightbox swipe down to close'
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
