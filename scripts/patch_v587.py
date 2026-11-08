#!/usr/bin/env python3
"""Patch v586 -> v587:
1. Equal spacing: reactions marginTop 4->6px to match bubble's 6px bottom padding
2. Fix emoji picker ✕ button: add onClick stopPropagation so the click doesn't
   bubble to the bubble div and toggle actions back off
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v586.js'
dst = '_deploy/assets/index-DUcNPOLc-v587.js'

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

# ── 1. Match spacing: reactions marginTop = bubble bottom padding (6px) ──
patch(
    'style:{marginTop:4,paddingLeft:0,paddingRight:0}',
    'style:{marginTop:6,paddingLeft:0,paddingRight:0}',
    'reactions marginTop 4->6px to match bubble bottom padding'
)

# ── 2. Fix ✕ button: add onClick stopPropagation to prevent bubble toggle ──
patch(
    'className:`chat-emoji-close-btn`,onMouseDown:(e)=>{e.preventDefault();x(!1);y(!0);},children:`✕`',
    'className:`chat-emoji-close-btn`,onMouseDown:(e)=>{e.preventDefault();x(!1);y(!0);},onClick:e=>e.stopPropagation(),children:`✕`',
    'emoji close button stops click propagation'
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
