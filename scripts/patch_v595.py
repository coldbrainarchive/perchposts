#!/usr/bin/env python3
"""Patch v594 -> v595: Animated spinner for attachment upload loading state."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v594.js'
dst = '_deploy/assets/index-DUcNPOLc-v595.js'

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

# ── 1. Inject @keyframes for spinner into CSS block ──
patch(
    '.chat-compose {\n        border-top: 1px solid rgba',
    '@keyframes _caSpin{to{transform:rotate(360deg)}}\n      .chat-compose {\n        border-top: 1px solid rgba',
    'inject spinner keyframe CSS'
)

# ── 2. Replace `…` text with animated SVG spinner in attach button ──
patch(
    'children:_cUL?`…`:(0,L.jsx)(`svg`,{width:12,height:12,viewBox:`0 0 12 12`,stroke:`currentC',
    'children:_cUL?(0,L.jsx)(`svg`,{width:16,height:16,viewBox:`0 0 16 16`,fill:`none`,style:{animation:`_caSpin 0.8s linear infinite`},children:(0,L.jsx)(`circle`,{cx:8,cy:8,r:6,stroke:`currentColor`,strokeWidth:2,strokeLinecap:`round`,strokeDasharray:`28`,strokeDashoffset:`10`})}):(0,L.jsx)(`svg`,{width:12,height:12,viewBox:`0 0 12 12`,stroke:`currentC',
    'animated spinner in attach button'
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
