#!/usr/bin/env python3
"""Patch v613 -> v617:
Fix Attach button spinner on new post page.
- onChange: call re(!0) synchronously before M() so React renders the spinner
  BEFORE the async upload starts (same pattern as comment attach _setCUL(!0))
- Button children: replace plain '...' with the same spinning SVG as comments
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v613.js'
dst = '_deploy/assets/index-DUcNPOLc-v617.js'

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

# ── 1. Fix onChange: set loading state synchronously before async M() ──
patch(
    'onChange:e=>e.target.files[0]&&M(e.target.files[0],e.target.files[0].type.startsWith(`video`)?`video`:`image`)',
    'onChange:e=>{if(e.target.files[0]){re(!0);M(e.target.files[0],e.target.files[0].type.startsWith(`video`)?`video`:`image`);}}',
    'set re(!0) synchronously in onChange before async M'
)

# ── 2. Replace '...' with spinning SVG (same as comment attach button) ──
patch(
    'children:ne?`…`:(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`span`,{style:{display:`inline-block`,transform:`scaleX(-1)`},children:`\U0001f4ce`}),` Attach`]})',
    'children:ne?(0,L.jsx)(`svg`,{width:14,height:14,viewBox:`0 0 16 16`,fill:`none`,style:{animation:`_caSpin 0.8s linear infinite`,verticalAlign:`middle`},children:(0,L.jsx)(`circle`,{cx:8,cy:8,r:6,stroke:`currentColor`,strokeWidth:2,strokeLinecap:`round`,strokeDasharray:`28`,strokeDashoffset:`10`})}):(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`span`,{style:{display:`inline-block`,transform:`scaleX(-1)`},children:`\U0001f4ce`}),` Attach`]})',
    'spinner SVG on Attach button while loading'
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
