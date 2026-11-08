#!/usr/bin/env python3
"""Patch v328 -> v329: move emoji picker row inside chat-bubble so it's wrapped by the bubble."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v328.js'
dst = '_deploy/assets/index-DUcNPOLc-v329.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Move emoji picker inside chat-bubble children ─────────────────────────
# Currently chat-bubble ends: ...span.chat-bubble-text]})  then emoji-picker is a sibling
# Move it in as the last child of chat-bubble, conditionally rendered on b
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
    'onMouseDown:(e)=>{e.preventDefault();x(!1);},children:`✕`})]})'
    ']})'
)
if OLD_BUBBLE_END in content:
    content = content.replace(OLD_BUBBLE_END, NEW_BUBBLE_END, 1)
    print('OK: emoji picker moved inside chat-bubble children')
else:
    errors.append('FAIL: chat-bubble end not found')

# ── 2. Remove the now-duplicate sibling emoji-picker-row ──────────────────────
OLD_SIBLING = (
    '(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`,'
    'style:{display:b?``:`none`},'
    'children:[(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onChange:O,onBlur:()=>x(!1)}),(0,L.jsx)(`button`,{className:`chat-emoji-close-btn`,'
    'onMouseDown:(e)=>{e.preventDefault();x(!1);},children:`✕`})]})'
)
if OLD_SIBLING in content:
    content = content.replace(OLD_SIBLING, '', 1)
    print('OK: removed duplicate sibling emoji picker row')
else:
    errors.append('FAIL: sibling emoji picker row not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
