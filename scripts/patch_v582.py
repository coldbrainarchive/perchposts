#!/usr/bin/env python3
"""Patch v581 -> v582:
1. Add top margin to action sheet so it has breathing room from text
2. Move emoji picker inside bubble (after action sheet, before reactions) so it replaces action buttons when React is tapped
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v581.js'
dst = '_deploy/assets/index-DUcNPOLc-v582.js'

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

EMOJI_PICKER = (
    'b&&(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`,children:['
    '(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,type:`text`,inputMode:`emoji`,'
    'placeholder:`Pick an emoji...`,onChange:O,onBlur:()=>x(!1)}),'
    '(0,L.jsx)(`button`,{className:`chat-emoji-close-btn`,onMouseDown:(e)=>{'
    'e.preventDefault();x(!1);y(!0);},children:`✕`})]})'
)

# ── 1. Add marginTop to action sheet CSS to separate it from text ──
patch(
    '.chat-action-sheet {\n        display: flex;\n        gap: 6px;\n        flex-wrap: wrap;\n        padding: 8px 14px;\n        background: #1e2530;\n        border-top: 1px solid rgba(148,163,184,0.1);',
    '.chat-action-sheet {\n        display: flex;\n        gap: 6px;\n        flex-wrap: wrap;\n        padding: 10px 14px 8px;\n        margin-top: 6px;\n        background: #1e2530;\n        border-top: 1px solid rgba(148,163,184,0.1);',
    'add margin-top to action sheet'
)

# ── 2. Insert emoji picker inside bubble after action sheet, before reactions ──
# Current: ...action_sheet,reactions,...   outside bubble: emoji_picker,bird
# New:     ...action_sheet,emoji_picker,reactions,...   outside bubble: bird only
patch(
    # Remove emoji picker from outside bubble
    EMOJI_PICKER + ',_birdOpen',
    ',_birdOpen',
    'remove emoji picker from outside bubble'
)

patch(
    # Insert emoji picker inside bubble between action sheet and reactions
    'v&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`',
    EMOJI_PICKER + ',v&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`',
    'insert emoji picker inside bubble before action sheet'
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
