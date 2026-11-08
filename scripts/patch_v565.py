#!/usr/bin/env python3
"""Patch v564 -> v565:
- Attach button: wrap + in span with lineHeight:1 + fontWeight:700 to center + match send boldness
- Video preview: add onLoadedMetadata seek to 0.1s so first frame always renders
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v564.js'
dst = '_deploy/assets/index-DUcNPOLc-v565.js'

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

# ── 1. Fix + centering + weight: wrap in span, fontWeight 700, lineHeight 1 ──
patch(
    'fontSize:18,fontWeight:300,cursor:_cUL||m?`default`:`pointer`,display:`flex`,alignItems:`center`,justifyContent:`center`,opacity:_cUL||m?0.45:1,transition:`background 0.15s,opacity 0.15s`},title:`Attach photo or video`,children:_cUL?`…`:`+`',
    'fontSize:20,fontWeight:700,cursor:_cUL||m?`default`:`pointer`,display:`flex`,alignItems:`center`,justifyContent:`center`,lineHeight:1,opacity:_cUL||m?0.45:1,transition:`background 0.15s,opacity 0.15s`},title:`Attach photo or video`,children:_cUL?`…`:(0,L.jsx)(`span`,{style:{lineHeight:1,display:`block`,marginTop:-2},children:`+`})',
    'fix + centering and weight'
)

# ── 2. Video preview: seek to first frame on metadata load ──
patch(
    'muted:!0,preload:`metadata`})',
    'muted:!0,preload:`metadata`,onLoadedMetadata:_ve=>{_ve.target.currentTime=0.1}})',
    'video preview seek to first frame'
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
