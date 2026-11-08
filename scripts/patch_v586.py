#!/usr/bin/env python3
"""Patch v585 -> v586:
1. Merge emoji picker + action sheet into one ternary slot so they truly swap
2. Tighten vertical spacing: 8px -> 4px margins/paddings throughout
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v585.js'
dst = '_deploy/assets/index-DUcNPOLc-v586.js'

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
    'b&&(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`,style:{background:`transparent`,borderTop:`none`,padding:`6px 0`},children:[(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,onChange:O,onBlur:()=>x(!1)}),(0,L.jsx)(`button`,{className:`chat-emoji-close-btn`,onMouseDown:(e)=>{e.preventDefault();x(!1);y(!0);},children:`✕`})]})'
)

ACTION_SHEET = (
    'v&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`,style:{background:`transparent`,borderTop:`none`,padding:`8px 0`},children:[(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),s&&s(e)},children:`Reply`}),(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:D,children:`React`}),e.parent_comment_id&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),d&&d(e.parent_comment_id)},children:`Find`}),a&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:e=>{e.stopPropagation(),y(!1),o&&o()},children:e.pinned?`Unpin`:`Pin`}),e.username&&!_isMe?((0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1);fetch(`${R}/user-stats?username=${encodeURIComponent(e.username)}`).then(r=>r.json()).then(d=>{_setBirdStats(d);_setBirdOpen(!0);}).catch(()=>_setBirdOpen(!0));},children:`Bird`})):null,r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:e=>{e.stopPropagation(),confirm(`Delete this comment?`)&&(y(!1),i())},children:`Delete`})]})'
)

# Action sheet with tighter padding
ACTION_SHEET_TIGHT = ACTION_SHEET.replace('padding:`8px 0`', 'padding:`4px 0`')

# Emoji picker with tighter padding
EMOJI_PICKER_TIGHT = EMOJI_PICKER.replace('padding:`6px 0`', 'padding:`4px 0`')

# ── 1. Merge into one ternary slot: b ? emoji_picker : v ? action_sheet : null ──
OLD_SLOT = EMOJI_PICKER + ',' + ACTION_SHEET
NEW_SLOT = 'b?' + EMOJI_PICKER_TIGHT + ':v?' + ACTION_SHEET_TIGHT + ':null'

patch(OLD_SLOT, NEW_SLOT, 'merge emoji+actions into single ternary slot')

# ── 2. Tighten reactions margin ──
patch(
    'style:{marginTop:8,paddingLeft:0,paddingRight:0}',
    'style:{marginTop:4,paddingLeft:0,paddingRight:0}',
    'tighten reactions marginTop'
)

# ── 3. Tighten attachment margin ──
patch(
    '(({attachment:_ca})=>_ca?(0,L.jsx)(`div`,{style:{marginTop:8},onClick:_ev=>_ev.stopPropagation()',
    '(({attachment:_ca})=>_ca?(0,L.jsx)(`div`,{style:{marginTop:4},onClick:_ev=>_ev.stopPropagation()',
    'tighten attachment marginTop'
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
