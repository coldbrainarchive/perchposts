#!/usr/bin/env python3
"""Patch v589 -> v590:
1. Action sheet container: add onClick stopPropagation so button clicks don't reach bubble
2. Emoji picker container: same
3. Reactions container: same (tapping a reaction shouldn't toggle actions)
4. Bubble onClick: simplify back to plain toggle (containers handle propagation)
5. Close ✕: add onTouchEnd with preventDefault to suppress mobile click event;
   keep onMouseDown for desktop — together these ensure close always shows actions
6. Spacing: action sheet padding 6px top only (remove 6px bottom, bubble provides it)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v589.js'
dst = '_deploy/assets/index-DUcNPOLc-v590.js'

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

# ── 1. Action sheet container: stop propagation ──
patch(
    'chat-action-sheet`,style:{background:`transparent`,borderTop:`none`,padding:`6px 0`},children:',
    'chat-action-sheet`,style:{background:`transparent`,borderTop:`none`,padding:`6px 0 0`},onClick:e=>e.stopPropagation(),children:',
    'action sheet stops click propagation + fix bottom padding'
)

# ── 2. Emoji picker container: stop propagation ──
patch(
    'chat-emoji-picker-row`,style:{background:`transparent`,borderTop:`none`,padding:`6px 0`},children:',
    'chat-emoji-picker-row`,style:{background:`transparent`,borderTop:`none`,padding:`6px 0 0`},onClick:e=>e.stopPropagation(),children:',
    'emoji picker stops click propagation + fix bottom padding'
)

# ── 3. Reactions container: stop propagation ──
patch(
    'className:`chat-reactions`,style:{marginTop:6,paddingLeft:0,paddingRight:0,paddingBottom:0},',
    'className:`chat-reactions`,style:{marginTop:6,paddingLeft:0,paddingRight:0,paddingBottom:0},onClick:e=>e.stopPropagation(),',
    'reactions stops click propagation'
)

# ── 4. Bubble onClick: simplify back to plain toggle ──
patch(
    'onClick:()=>!p&&(b?(x(!1),void 0):y(_s=>!_s)),',
    'onClick:()=>!p&&y(_s=>!_s),',
    'simplify bubble onClick'
)

# ── 5. Close ✕: add onTouchEnd to suppress mobile click + keep state correct ──
patch(
    'onMouseDown:(e)=>{e.preventDefault();e.stopPropagation();x(!1);y(!0);},children:`✕`',
    'onMouseDown:(e)=>{e.preventDefault();e.stopPropagation();x(!1);y(!0);},onTouchEnd:(e)=>{e.preventDefault();e.stopPropagation();x(!1);y(!0);},children:`✕`',
    'close button: onTouchEnd suppresses mobile click'
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
