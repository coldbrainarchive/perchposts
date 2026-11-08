#!/usr/bin/env python3
"""Patch v613 -> v614:
Add fade+scale-up animation when an attachment loads on the new post page.
- Adds @keyframes _ppIn CSS animation
- Applies it to the attachment preview wrapper div
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v613.js'
dst = '_deploy/assets/index-DUcNPOLc-v614.js'

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

# ── 1. Add @keyframes _ppIn alongside _caSpin ──
patch(
    '@keyframes _caSpin{to{transform:rotate(360deg)}}',
    '@keyframes _caSpin{to{transform:rotate(360deg)}}@keyframes _ppIn{from{opacity:0;transform:scale(0.92)}to{opacity:1;transform:scale(1)}}',
    'add _ppIn keyframe'
)

# ── 2. Apply animation to attachment preview wrapper on new post page ──
patch(
    'T&&(0,L.jsxs)(`div`,{style:{marginTop:10,position:`relative`},children:[(0,L.jsx)(Fr,{attachment:T})',
    'T&&(0,L.jsxs)(`div`,{style:{marginTop:10,position:`relative`,animation:`_ppIn 0.25s ease-out`},children:[(0,L.jsx)(Fr,{attachment:T})',
    'apply _ppIn animation to post attachment preview'
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
