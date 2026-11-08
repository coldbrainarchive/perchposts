#!/usr/bin/env python3
"""Patch v578 -> v584: Full bubble restructure (clean start).
Order inside bubble: text → reactions → emoji_picker|action_sheet → attachment
- Attachment tap stops propagation (doesn't open actions)
- Tap username opens actions
- Transparent action sheet / emoji picker (no dark bg or border)
- Uniform 8px spacing between elements
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v578.js'
dst = '_deploy/assets/index-DUcNPOLc-v584.js'

content = open(src, encoding='utf-8').read()

# ── Extract exact live blocks from v578 ──────────────────────────────────────

iife_end_marker = ')( Mr(e.content))'
idx = content.find('(({text:_ct,attachment:_ca})=>(0,L.jsxs)(L.Fragment')
TEXT_IIFE_OLD = content[idx : content.find(iife_end_marker, idx) + len(iife_end_marker)]

idx2 = content.find('ee.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`')
REACTIONS = content[idx2 : content.find('}),v&&', idx2) + 2]

idx3 = content.find('v&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`')
ACTION_SHEET = content[idx3 : content.find('),b&&', idx3) + 1]

idx4 = content.find('b&&(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`')
EMOJI_PICKER = content[idx4 : content.find('),_birdOpen', idx4) + 1]

# ── Build new components ─────────────────────────────────────────────────────

# Text-only IIFE (no attachment)
TEXT_ONLY = (
    '(({text:_ct})=>_ct'
    '?(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct})'
    ':null)(Mr(e.content))'
)

# Reactions with uniform top margin
REACTIONS_NEW = REACTIONS.replace(
    '`div`,{className:`chat-reactions`',
    '`div`,{className:`chat-reactions`,style:{marginTop:8}'
)

# Action sheet — transparent bg, no border, even padding
ACTION_SHEET_NEW = ACTION_SHEET.replace(
    '`div`,{className:`chat-action-sheet`,children:',
    '`div`,{className:`chat-action-sheet`,style:{background:`transparent`,borderTop:`none`,padding:`8px 14px`},children:'
)

# Emoji picker — transparent bg, no border, even padding
EMOJI_PICKER_NEW = EMOJI_PICKER.replace(
    '`div`,{className:`chat-emoji-picker-row`,children:',
    '`div`,{className:`chat-emoji-picker-row`,style:{background:`transparent`,borderTop:`none`,padding:`6px 14px`},children:'
)

# Attachment IIFE with marginTop:8 and stopPropagation (no bubble toggle)
ATTACH_NEW = (
    '(({attachment:_ca})=>_ca'
    '?(0,L.jsx)(`div`,{style:{marginTop:8},onClick:_ev=>_ev.stopPropagation(),'
    'children:(0,L.jsx)(Fr,{attachment:_ca})})'
    ':null)(Mr(e.content))'
)

# ── OLD sequence: IIFE inside bubble + bubble close + reactions + action sheet + emoji picker ──
OLD = (
    TEXT_IIFE_OLD +
    ']})' +          # closes bubble children [] + bubble jsx call
    ',' + REACTIONS +
    ',' + ACTION_SHEET +
    ',' + EMOJI_PICKER +
    ',_birdOpen'
)

# ── NEW sequence: all inside bubble, then bird modal ──
NEW = (
    TEXT_ONLY +
    ',' + REACTIONS_NEW +
    ',' + EMOJI_PICKER_NEW +
    ',' + ACTION_SHEET_NEW +
    ',' + ATTACH_NEW +
    ']})' +          # closes bubble children [] + bubble jsx call
    ',_birdOpen'
)

errors = []
n = content.count(OLD)
if n == 0:
    errors.append('FAIL: OLD sequence not found')
elif n > 1:
    errors.append(f'FAIL: {n} matches')
else:
    content = content.replace(OLD, NEW)
    print('OK: restructured bubble contents')

# ── Add onClick to chat-msg-meta (tap username opens actions) ────────────────
META_OLD = 'className:`chat-msg-meta`,style:{background:e.is_admin===true?`#ffffff`:h}'
META_NEW = 'className:`chat-msg-meta`,onClick:()=>!p&&y(_s=>!_s),style:{cursor:`pointer`,background:e.is_admin===true?`#ffffff`:h}'
n2 = content.count(META_OLD)
if n2 == 0:
    errors.append('FAIL: meta onClick not found')
elif n2 > 1:
    errors.append(f'FAIL: meta {n2} matches')
else:
    content = content.replace(META_OLD, META_NEW)
    print('OK: tap username opens actions')

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
