#!/usr/bin/env python3
"""Patch v330 -> v331:
- Put emoji picker INSIDE chat-bubble (so bubble border wraps it)
- Action sheet stays outside bubble, hidden when emoji picker is open
- X button closes emoji picker and reopens action sheet
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v330.js'
dst = '_deploy/assets/index-DUcNPOLc-v331.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Move emoji picker inside the bubble as last child ─────────────────────
OLD_BUBBLE_END = (
    '(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:e.content})]})'
)
NEW_BUBBLE_END = (
    '(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:e.content}),'
    'b&&(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`,'
    'children:[(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onChange:O,onBlur:()=>x(!1),onClick:(e)=>e.stopPropagation()}),'
    '(0,L.jsx)(`button`,{className:`chat-emoji-close-btn`,'
    'onMouseDown:(e)=>{e.preventDefault();x(!1);y(!0);},children:`✕`})]})'
    ']})'
)
if OLD_BUBBLE_END in content:
    content = content.replace(OLD_BUBBLE_END, NEW_BUBBLE_END, 1)
    print('OK: emoji picker moved inside chat-bubble')
else:
    errors.append('FAIL: bubble end not found')

# ── 2. Remove the sibling emoji picker that was added in v330 ─────────────────
OLD_SIBLING = (
    ',b&&(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`,'
    'children:[(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onChange:O,onBlur:()=>x(!1)}),'
    '(0,L.jsx)(`button`,{className:`chat-emoji-close-btn`,'
    'onMouseDown:(e)=>{e.preventDefault();x(!1);y(!0);},children:`✕`})]})'
)
if OLD_SIBLING in content:
    content = content.replace(OLD_SIBLING, '', 1)
    print('OK: removed sibling emoji picker')
else:
    errors.append('FAIL: sibling emoji picker not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
