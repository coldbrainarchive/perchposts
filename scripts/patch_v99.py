#!/usr/bin/env python3
"""Patch v98 -> v99: centre text independently from the bird emoji."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v98.js'
dst = '_deploy/assets/index-DUcNPOLc-v99.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Outer div: add position:relative + justifyContent:center, remove gap ───
OLD_OUTER_STYLE = 'display:`flex`,alignItems:`center`,gap:8,padding:`9px 12px`'
NEW_OUTER_STYLE = 'display:`flex`,alignItems:`center`,justifyContent:`center`,position:`relative`,padding:`9px 12px`'
if OLD_OUTER_STYLE in content:
    content = content.replace(OLD_OUTER_STYLE, NEW_OUTER_STYLE, 1)
    print('OK: outer div - added position:relative + justifyContent:center, removed gap')
else:
    errors.append('FAIL: outer div style not found')

# ── 2. Emoji span: absolutely position it on the left ────────────────────────
OLD_EMOJI = '(0,L.jsx)(`span`,{style:{fontSize:18},children:`\U0001f424`})'
NEW_EMOJI = '(0,L.jsx)(`span`,{style:{position:`absolute`,left:12,fontSize:18,lineHeight:1},children:`\U0001f424`})'
if OLD_EMOJI in content:
    content = content.replace(OLD_EMOJI, NEW_EMOJI, 1)
    print('OK: emoji span - absolutely positioned left')
else:
    errors.append('FAIL: emoji span not found')

# ── 3. Text span: remove flex:1/overflow, add textAlign:center ───────────────
OLD_TEXT = (
    '(0,L.jsx)(`span`,{style:{flex:1,fontSize:14,fontWeight:700,'
    'color:_gu?Hn(null,_gu):`#64748b`,'
    'letterSpacing:`-0.01em`,'
    'overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`'
    '},children:_gu||`tap to generate username`})'
)
NEW_TEXT = (
    '(0,L.jsx)(`span`,{style:{fontSize:14,fontWeight:700,'
    'color:_gu?Hn(null,_gu):`#64748b`,'
    'letterSpacing:`-0.01em`,'
    'textAlign:`center`'
    '},children:_gu||`tap to generate username`})'
)
if OLD_TEXT in content:
    content = content.replace(OLD_TEXT, NEW_TEXT, 1)
    print('OK: text span - centered, flex/overflow removed')
else:
    errors.append('FAIL: text span not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
