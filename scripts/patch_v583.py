#!/usr/bin/env python3
"""Patch v582 -> v583:
1. Action sheet: transparent bg, no border-top, even padding via inline style
2. Emoji picker row: same inline style treatment
3. Reactions: add consistent marginTop so spacing is even
4. Attachment: consistent marginTop
5. Add onClick to chat-msg-meta (tap name opens actions)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v582.js'
dst = '_deploy/assets/index-DUcNPOLc-v583.js'

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

# ── 1. Action sheet: transparent bg, no border, even 8px vertical padding ──
patch(
    '(0,L.jsxs)(`div`,{className:`chat-action-sheet`,children:',
    '(0,L.jsxs)(`div`,{className:`chat-action-sheet`,style:{background:`transparent`,borderTop:`none`,padding:`8px 14px`},children:',
    'action sheet transparent bg + even padding'
)

# ── 2. Emoji picker row: transparent bg, no border ──
patch(
    '(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`,children:',
    '(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`,style:{background:`transparent`,borderTop:`none`,padding:`8px 14px 4px`},children:',
    'emoji picker row transparent bg'
)

# ── 3. Reactions: add marginTop:8 for even gap from text ──
patch(
    'ee.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`,',
    'ee.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`,style:{marginTop:8},',
    'reactions marginTop'
)

# ── 4. Attachment: consistent marginTop:8 (was 6) ──
patch(
    '(({attachment:_ca})=>_ca?(0,L.jsx)(`div`,{style:{marginTop:6},children:(0,L.jsx)(Fr,{attachment:_ca})}):null)',
    '(({attachment:_ca})=>_ca?(0,L.jsx)(`div`,{style:{marginTop:8},children:(0,L.jsx)(Fr,{attachment:_ca})}):null)',
    'attachment marginTop consistent'
)

# ── 5. Add onClick to chat-msg-meta so tapping name opens actions ──
patch(
    'className:`chat-msg-meta`,style:{background:e.is_admin===true?`#ffffff`:h}',
    'className:`chat-msg-meta`,onClick:()=>!p&&y(_s=>!_s),style:{cursor:`pointer`,background:e.is_admin===true?`#ffffff`:h}',
    'tap name opens actions'
)

# ── 6. Clean up old margin-top added in v582 since we handle it via inline now ──
patch(
    '.chat-action-sheet {\n        display: flex;\n        gap: 6px;\n        flex-wrap: wrap;\n        padding: 10px 14px 8px;\n        margin-top: 6px;\n        background: #1e2530;\n        border-top: 1px solid rgba(148,163,184,0.1);',
    '.chat-action-sheet {\n        display: flex;\n        gap: 6px;\n        flex-wrap: wrap;\n        padding: 8px 14px;\n        background: #1e2530;\n        border-top: 1px solid rgba(148,163,184,0.1);',
    'revert action sheet CSS margin-top (handled inline now)'
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
