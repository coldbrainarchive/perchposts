#!/usr/bin/env python3
"""Patch v584 -> v585:
- Left-align reactions, action sheet, and emoji picker with the text body
  (bubble has 10px left padding; these elements need 0 horizontal padding of their own)
- Emoji picker: keep it replacing action sheet (already correct order in DOM)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v584.js'
dst = '_deploy/assets/index-DUcNPOLc-v585.js'

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

# ── 1. Reactions: remove left/right padding so pills align with text ──
patch(
    'className:`chat-reactions`,style:{marginTop:8}',
    'className:`chat-reactions`,style:{marginTop:8,paddingLeft:0,paddingRight:0}',
    'reactions left-align with text'
)

# ── 2. Action sheet: 0 horizontal padding (bubble provides 10px) ──
patch(
    'chat-action-sheet`,style:{background:`transparent`,borderTop:`none`,padding:`8px 14px`}',
    'chat-action-sheet`,style:{background:`transparent`,borderTop:`none`,padding:`8px 0`}',
    'action sheet left-align with text'
)

# ── 3. Emoji picker: 0 horizontal padding ──
patch(
    'chat-emoji-picker-row`,style:{background:`transparent`,borderTop:`none`,padding:`6px 14px`}',
    'chat-emoji-picker-row`,style:{background:`transparent`,borderTop:`none`,padding:`6px 0`}',
    'emoji picker left-align with text'
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
