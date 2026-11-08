#!/usr/bin/env python3
"""Patch v283 -> v284:
1. Wrap b.map (countries) in flex div with gap
2. Wrap UR.map (users) in flex div with gap
3. Fix admin hat bird img so pill stays same height as others
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v283.js'
dst = '_deploy/assets/index-DUcNPOLc-v284.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Wrap countries b.map in a flex div with gap ────────────────────────────
OLD_BMAP = (
    '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Countries`}),'
    'b.map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>k(e.name),children:(0,L.jsx)(kr,{country:e.name,small:!0})},e.name))'
)
NEW_BMAP = (
    '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Countries`}),'
    '(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:8,padding:`4px 14px 6px`},'
    'children:b.map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>k(e.name),children:(0,L.jsx)(kr,{country:e.name,small:!0})},e.name))})'
)
if OLD_BMAP in content:
    content = content.replace(OLD_BMAP, NEW_BMAP, 1)
    print('OK: countries wrapped in flex div with gap')
else:
    errors.append('FAIL: countries b.map not found')

# ── 2. Wrap UR.map (users) in flex div — modify both opening and closing ──────
# Opening: wrap UR.map in a div
OLD_URMAP_OPEN = (
    '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Users`}),'
    'UR.map(_u=>(0,L.jsxs)(`button`,{className:`search-suggestion`'
)
NEW_URMAP_OPEN = (
    '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Users`}),'
    '(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:8,padding:`4px 14px 6px`},'
    'children:UR.map(_u=>(0,L.jsxs)(`button`,{className:`search-suggestion`'
)
if OLD_URMAP_OPEN in content:
    content = content.replace(OLD_URMAP_OPEN, NEW_URMAP_OPEN, 1)
    print('OK: users flex div opened')
else:
    errors.append('FAIL: users UR.map opening not found')

# Closing: after UR.map closes (]}) for users Fragment), add }) to close flex div
# From tracing: end sequence is _u.username)) + ]}, + [3x]}) + }) + }
OLD_URMAP_CLOSE = '_u.username))' + ']}),' + ']})' * 3 + '})' + '}'
# flex div closes (}) BEFORE Fragment closes (]}) — flex div is child of Fragment
NEW_URMAP_CLOSE = '_u.username))' + '})' + ']}),' + ']})' * 3 + '})' + '}'
if OLD_URMAP_CLOSE in content:
    content = content.replace(OLD_URMAP_CLOSE, NEW_URMAP_CLOSE, 1)
    print('OK: users flex div closed')
else:
    errors.append('FAIL: users flex div closing not found')

# ── 3. Fix admin hat bird img height so pill aligns with others ───────────────
OLD_ADMIN_IMG = (
    '`admin`?(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'style:{height:14,width:`auto`,display:`block`}})'
)
NEW_ADMIN_IMG = (
    '`admin`?(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'style:{height:16,width:16,objectFit:`contain`,display:`block`,flexShrink:0}})'
)
if OLD_ADMIN_IMG in content:
    content = content.replace(OLD_ADMIN_IMG, NEW_ADMIN_IMG)
    print('OK: admin img fixed to 16x16')
else:
    print('NOTE: admin img style not found — may already be fixed')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
