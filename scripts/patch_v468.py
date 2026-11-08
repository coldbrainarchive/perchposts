#!/usr/bin/env python3
"""Patch v467 -> v468:
Make the comment bubble meta header match the search bar pill visually.
- Override padding to 0 9px 0 6px (pill padding) and height to 22px
- Bird: _bsz+2 → _bsz (same as pill badges), width/height 17px → 16px
- Username: fontSize:11 → fontSize:12 (matches .user-pill font-size:12px)
- Admin bird img: height:17px → 16px
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v467.js'
dst = '_deploy/assets/index-DUcNPOLc-v468.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Meta div: add padding + height to inline style ─────────────────────────
OLD_META = 'className:`chat-msg-meta`,style:{background:e.is_admin===true?`#ffffff`:h}'
NEW_META = 'className:`chat-msg-meta`,style:{background:e.is_admin===true?`#ffffff`:h,padding:`0 9px 0 6px`,height:`22px`,boxSizing:`border-box`}'
if OLD_META in content:
    content = content.replace(OLD_META, NEW_META, 1)
    print('OK: meta padding/height set to pill values')
else:
    errors.append('FAIL: chat-msg-meta style not found')

# ── 2. Admin bird img: 17px → 16px ────────────────────────────────────────────
OLD_ADM = 'style:{height:`17px`,width:`auto`,flexShrink:0,display:`block`}'
NEW_ADM = 'style:{height:`16px`,width:`auto`,flexShrink:0,display:`block`}'
if OLD_ADM in content:
    content = content.replace(OLD_ADM, NEW_ADM, 1)
    print('OK: admin bird height 17→16')
else:
    errors.append('FAIL: admin bird img not found')

# ── 3. Bird span: _bsz+2 / 17px → _bsz / 16px ───────────────────────────────
OLD_BIRD = 'fontSize:_bsz+2,lineHeight:1,flexShrink:0,width:`17px`,height:`17px`'
NEW_BIRD = 'fontSize:_bsz,lineHeight:1,flexShrink:0,width:`16px`,height:`16px`'
if OLD_BIRD in content:
    content = content.replace(OLD_BIRD, NEW_BIRD, 1)
    print('OK: comment bird fontSize _bsz+2→_bsz, size 17→16')
else:
    errors.append('FAIL: comment bird span not found')

# ── 4. Username: fontSize:11 → 12 ─────────────────────────────────────────────
OLD_UN = 'style:{fontWeight:700,fontSize:11,color:`#0a0a0a`,whiteSpace:`nowrap`}'
NEW_UN = 'style:{fontWeight:700,fontSize:12,color:`#0a0a0a`,whiteSpace:`nowrap`}'
if OLD_UN in content:
    content = content.replace(OLD_UN, NEW_UN, 1)
    print('OK: username fontSize 11→12')
else:
    errors.append('FAIL: username span not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
