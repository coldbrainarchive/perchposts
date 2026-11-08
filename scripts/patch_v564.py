#!/usr/bin/env python3
"""Patch v563 -> v564:
- Attach button: match send button exactly (36px circle, purple when active, gray-translucent when idle, "+" icon)
- Video attachment preview: add preload="metadata" so first frame renders as thumbnail
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v563.js'
dst = '_deploy/assets/index-DUcNPOLc-v564.js'

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

# ── 1. Restyle attach button to match send button ──
patch(
    'style:{flexShrink:0,width:32,height:32,borderRadius:999,border:`1px solid rgba(255,255,255,0.08)`,background:_cA?`rgba(192,132,252,0.15)`:`rgba(255,255,255,0.05)`,color:_cA?`#c084fc`:`rgba(255,255,255,0.35)`,fontSize:15,cursor:_cUL||m?`default`:`pointer`,display:`flex`,alignItems:`center`,justifyContent:`center`,transition:`background 0.15s,color 0.15s`},title:`Attach photo or video`,children:_cUL?(0,L.jsx)(`span`,{style:{fontSize:11},children:`…`}):`📎`',
    'style:{flexShrink:0,width:36,height:36,borderRadius:999,border:`none`,background:_cA?`#7c3aed`:`rgba(255,255,255,0.08)`,color:`#fff`,fontSize:18,fontWeight:300,cursor:_cUL||m?`default`:`pointer`,display:`flex`,alignItems:`center`,justifyContent:`center`,opacity:_cUL||m?0.45:1,transition:`background 0.15s,opacity 0.15s`},title:`Attach photo or video`,children:_cUL?`…`:`+`',
    'attach button matches send button style with + icon'
)

# ── 2. Video preview: add preload=metadata so first frame shows ──
patch(
    '(0,L.jsx)(`video`,{src:_cA.url,style:{maxHeight:72,maxWidth:128,borderRadius:8},muted:!0})',
    '(0,L.jsx)(`video`,{src:_cA.url,style:{maxHeight:72,maxWidth:128,borderRadius:8},muted:!0,preload:`metadata`})',
    'video preview preload metadata'
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
