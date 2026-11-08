#!/usr/bin/env python3
"""Patch v587 -> v588:
1. Reactions: zero out paddingBottom (CSS class has 8px bottom padding causing extra space)
2. Remove onBlur from emoji input (mobile: onBlur fires before mousedown, removes picker
   from DOM so click lands on bubble and toggles actions off)
3. Bubble onClick: if emoji picker open, close it instead of toggling actions
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v587.js'
dst = '_deploy/assets/index-DUcNPOLc-v588.js'

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

# ── 1. Zero reactions paddingBottom so bubble's own 6px is the only bottom gap ──
patch(
    'style:{marginTop:6,paddingLeft:0,paddingRight:0}',
    'style:{marginTop:6,paddingLeft:0,paddingRight:0,paddingBottom:0}',
    'zero reactions paddingBottom'
)

# ── 2. Remove onBlur from emoji input ──
patch(
    '`Pick an emoji...`,onChange:O,onBlur:()=>x(!1)})',
    '`Pick an emoji...`,onChange:O})',
    'remove onBlur from emoji input'
)

# ── 3. Bubble onClick: close emoji picker if open, otherwise toggle actions ──
patch(
    'className:`chat-bubble${p?` pending`:``}`,onClick:()=>!p&&y(e=>!e),',
    'className:`chat-bubble${p?` pending`:``}`,onClick:()=>!p&&(b?(x(!1),void 0):y(_s=>!_s)),',
    'bubble onClick closes emoji picker if open'
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
