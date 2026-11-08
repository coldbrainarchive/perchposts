#!/usr/bin/env python3
"""Patch v601 -> v602:
- Replace left-aligned 'Loading preview…' text with centered animated SVG spinner
- Wrap link preview Fr in compose area with pointerEvents:'none' to disable interactivity
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v601.js'
dst = '_deploy/assets/index-DUcNPOLc-v602.js'

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

# ── 1. Replace loading text with centered spinner ──
patch(
    '(_lpLoading&&!_cA)&&(0,L.jsx)(`div`,{style:{padding:`6px 12px 0`,fontSize:11,color:`#8fa0b6`},children:`Loading preview…`})',
    '(_lpLoading&&!_cA)&&(0,L.jsx)(`div`,{style:{padding:`6px 12px 0`,display:`flex`,justifyContent:`center`,alignItems:`center`,height:48},children:(0,L.jsx)(`svg`,{width:24,height:24,viewBox:`0 0 24 24`,fill:`none`,style:{animation:`_caSpin 0.8s linear infinite`},children:(0,L.jsx)(`circle`,{cx:12,cy:12,r:9,stroke:`#8fa0b6`,strokeWidth:2.5,strokeLinecap:`round`,strokeDasharray:`42`,strokeDashoffset:`14`})})})',
    'replace loading text with centered spinner'
)

# ── 2. Wrap Fr in compose preview with pointerEvents:none ──
patch(
    '(_lpAt&&!_cA)&&(0,L.jsxs)(`div`,{style:{padding:`6px 12px 0`,position:`relative`},children:[(0,L.jsx)(Fr,{attachment:_lpAt}),(0,L.jsx)(`button`',
    '(_lpAt&&!_cA)&&(0,L.jsxs)(`div`,{style:{padding:`6px 12px 0`,position:`relative`},children:[(0,L.jsx)(`div`,{style:{pointerEvents:`none`},children:(0,L.jsx)(Fr,{attachment:_lpAt})}),(0,L.jsx)(`button`',
    'wrap Fr in compose preview with pointerEvents none'
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
