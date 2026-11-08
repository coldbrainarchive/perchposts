#!/usr/bin/env python3
"""Patch v329 -> v330:
- Move emoji picker out of bubble, back as sibling of action-sheet
- X button reopens action sheet (they replace each other)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v329.js'
dst = '_deploy/assets/index-DUcNPOLc-v330.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove emoji picker from inside the bubble, restore clean bubble end ───
OLD_BUBBLE_END = (
    '(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:e.content}),'
    'b&&(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`,'
    'children:[(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onChange:O,onBlur:()=>x(!1),onClick:(e)=>e.stopPropagation()}),'
    '(0,L.jsx)(`button`,{className:`chat-emoji-close-btn`,'
    'onMouseDown:(e)=>{e.preventDefault();x(!1);},children:`✕`})]})'
    ']})'
)
NEW_BUBBLE_END = (
    '(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:e.content})]})'
)
if OLD_BUBBLE_END in content:
    content = content.replace(OLD_BUBBLE_END, NEW_BUBBLE_END, 1)
    print('OK: emoji picker removed from inside bubble')
else:
    errors.append('FAIL: bubble end with embedded emoji picker not found')

# ── 2. Add emoji picker as sibling after action-sheet, X reopens action sheet ─
OLD_ACTION_END = (
    'r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:e=>{e.stopPropagation(),confirm(`Delete this comment?`)&&(y(!1),i())},'
    'children:`Delete`})]})'
)
NEW_ACTION_END = (
    'r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:e=>{e.stopPropagation(),confirm(`Delete this comment?`)&&(y(!1),i())},'
    'children:`Delete`})]})'
    ',b&&(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`,'
    'children:[(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onChange:O,onBlur:()=>x(!1)}),'
    '(0,L.jsx)(`button`,{className:`chat-emoji-close-btn`,'
    'onMouseDown:(e)=>{e.preventDefault();x(!1);y(!0);},children:`✕`})]})'
)
if OLD_ACTION_END in content:
    content = content.replace(OLD_ACTION_END, NEW_ACTION_END, 1)
    print('OK: emoji picker added as action-sheet sibling, X reopens action sheet')
else:
    errors.append('FAIL: action sheet end not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
