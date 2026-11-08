#!/usr/bin/env python3
"""Patch v592 -> v593:
1. Add maxH prop to Fr (PostAttachment) — defaults 400, comments pass 240
2. Comment attachment call: pass maxH:240 for smaller thumbnails
3. Ensure bubble bottom is tappable: stopPropagation only on inner Fr div,
   add a small tap-zone row below attachment when no text exists
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v592.js'
dst = '_deploy/assets/index-DUcNPOLc-v593.js'

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

# ── 1. Add maxH prop to Fr signature ──
patch(
    'function Fr({attachment:e,postId:o})',
    'function Fr({attachment:e,postId:o,maxH:_mh=400})',
    'add maxH prop to Fr'
)

# ── 2. Use _mh for image maxHeight ──
patch(
    'display:`block`,maxHeight:400,objectFit:`cover`,cursor:`zoom-in`}',
    'display:`block`,maxHeight:_mh,objectFit:`cover`,cursor:`zoom-in`}',
    'image uses _mh'
)

# ── 3. Use _mh for video maxHeight (in bubble — display:block version) ──
patch(
    'maxWidth:`100%`,borderRadius:10,maxHeight:400,display:`block`}})',
    'maxWidth:`100%`,borderRadius:10,maxHeight:_mh,display:`block`}})',
    'video uses _mh'
)

# ── 4. Comment attachment: pass maxH:240 + add tap zone below when no text ──
patch(
    'onClick:_ev=>_ev.stopPropagation(),children:(0,L.jsx)(Fr,{attachment:_ca})}),_ct&&(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct})',
    'onClick:_ev=>_ev.stopPropagation(),children:(0,L.jsx)(Fr,{attachment:_ca,maxH:240})}),_ct?(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct}):(0,L.jsx)(`div`,{style:{height:16}})',
    'comment uses maxH:240 and adds tap zone below when no text'
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
