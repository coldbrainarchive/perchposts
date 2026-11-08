#!/usr/bin/env python3
"""Patch v94 -> v95:
- Remove clipboard button from signup area
- Use Hn(null,_gu) for pill color so user sees their actual post color
- Purple/white restricted by existing Hn hue-shift (250-320 already excluded)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v94.js'
dst = '_deploy/assets/index-DUcNPOLc-v95.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Replace hardcoded purple border with dynamic Hn color ──────────────────
OLD_BORDER = 'border:_gu?`1.5px solid #c084fc55`:`1.5px dashed #3f4756`'
NEW_BORDER = 'border:_gu?`1.5px solid ${Hn(null,_gu)}55`:`1.5px dashed #3f4756`'
if OLD_BORDER in content:
    content = content.replace(OLD_BORDER, NEW_BORDER, 1)
    print('OK: border color -> Hn dynamic')
else:
    errors.append('FAIL: border color not found')

# ── 2. Replace hardcoded purple background ────────────────────────────────────
OLD_BG = 'background:_gu?`#c084fc18`:`transparent`'
NEW_BG = 'background:_gu?`${Hn(null,_gu)}18`:`transparent`'
if OLD_BG in content:
    content = content.replace(OLD_BG, NEW_BG, 1)
    print('OK: background color -> Hn dynamic')
else:
    errors.append('FAIL: background color not found')

# ── 3. Replace hardcoded purple text color ────────────────────────────────────
OLD_COLOR = 'color:_gu?`#c084fc`:`#64748b`'
NEW_COLOR = 'color:_gu?Hn(null,_gu):`#64748b`'
if OLD_COLOR in content:
    content = content.replace(OLD_COLOR, NEW_COLOR, 1)
    print('OK: text color -> Hn dynamic')
else:
    errors.append('FAIL: text color not found')

# ── 4. Remove clipboard button entirely ──────────────────────────────────────
OLD_CLIP = (
    '_gu?(0,L.jsx)(`button`,{onClick:function(ev){try{navigator.clipboard.writeText(_gu);'
    'var b=ev.currentTarget;b.textContent="✓";b.style.color="#22c55e";'
    'setTimeout(function(){b.textContent="\U0001f4cb";b.style.color="#64748b"},1500)'
    '}catch(err){}},style:{background:`transparent`,border:`none`,cursor:`pointer`,'
    'color:`#64748b`,fontSize:14,padding:`0 2px`,lineHeight:1,flexShrink:0},'
    'children:`\U0001f4cb`}):null'
)
NEW_CLIP = ''
if OLD_CLIP in content:
    content = content.replace(OLD_CLIP, NEW_CLIP, 1)
    print('OK: clipboard button removed')
else:
    errors.append('FAIL: clipboard button not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
