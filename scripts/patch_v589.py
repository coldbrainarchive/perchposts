#!/usr/bin/env python3
"""Patch v588 -> v589:
1. Even spacing: action sheet + emoji picker padding 4px->6px to match text->reactions gap
2. Fix emoji picker close: ✕ onMouseDown must also stopPropagation to prevent bubble
   onClick from firing and closing everything; also restore actions on close
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v588.js'
dst = '_deploy/assets/index-DUcNPOLc-v589.js'

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

# ── 1. Even spacing: 4px → 6px on action sheet and emoji picker ──
patch(
    'chat-action-sheet`,style:{background:`transparent`,borderTop:`none`,padding:`4px 0`}',
    'chat-action-sheet`,style:{background:`transparent`,borderTop:`none`,padding:`6px 0`}',
    'action sheet padding 4->6px'
)
patch(
    'chat-emoji-picker-row`,style:{background:`transparent`,borderTop:`none`,padding:`4px 0`}',
    'chat-emoji-picker-row`,style:{background:`transparent`,borderTop:`none`,padding:`6px 0`}',
    'emoji picker padding 4->6px'
)

# ── 2. Fix ✕ close: stopPropagation on mousedown so bubble onClick never fires ──
# Current: e.preventDefault(); x(!1); y(!0);
# Need:    e.preventDefault(); e.stopPropagation(); x(!1); y(!0);
patch(
    'onMouseDown:(e)=>{e.preventDefault();x(!1);y(!0);},onClick:e=>e.stopPropagation()',
    'onMouseDown:(e)=>{e.preventDefault();e.stopPropagation();x(!1);y(!0);}',
    'fix close: stopPropagation on mousedown, remove redundant onClick'
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
