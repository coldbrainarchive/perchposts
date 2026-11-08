#!/usr/bin/env python3
"""Patch v254 -> v255: UserCard — add USER label, smaller/compact, purple Message button."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v254.js'
dst = '_deploy/assets/index-DUcNPOLc-v255.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add 🐦 USER label to left column (before bird) ────────────────────────
OLD_LEFT = 'justifyContent:`center`,gap:8,padding:`14px 12px`},children:[_bd&&_bd.hat?'
NEW_LEFT = (
    'justifyContent:`center`,gap:6,padding:`10px 10px`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.06em`},children:`\U0001f426 User`}),'
    '_bd&&_bd.hat?'
)
if OLD_LEFT in content:
    content = content.replace(OLD_LEFT, NEW_LEFT, 1)
    print('OK: USER label added to left column')
else:
    errors.append('FAIL: left column anchor not found')

# ── 2. Shrink bird size (40→32), admin bird (54→36→28), right column padding ─
OLD_BIRD_SZ = 'fontSize:40,lineHeight:1},'
NEW_BIRD_SZ = 'fontSize:32,lineHeight:1},'
if OLD_BIRD_SZ in content:
    content = content.replace(OLD_BIRD_SZ, NEW_BIRD_SZ, 1)
    print('OK: bird shrunk to 32px')
else:
    errors.append('FAIL: bird fontSize not found')

OLD_SPELS = '_spEls(_bd.s,40)'
NEW_SPELS = '_spEls(_bd.s,32)'
if OLD_SPELS in content:
    content = content.replace(OLD_SPELS, NEW_SPELS, 1)
    print('OK: _spEls updated to 32')
else:
    errors.append('FAIL: _spEls size not found')

# Shrink right column padding too
OLD_RIGHT_PAD = 'justifyContent:`center`,gap:8,padding:`14px 12px`},children:[(0,L.jsx)(`div`,{style:{fontSize:10'
NEW_RIGHT_PAD = 'justifyContent:`center`,gap:6,padding:`10px 10px`},children:[(0,L.jsx)(`div`,{style:{fontSize:10'
if OLD_RIGHT_PAD in content:
    content = content.replace(OLD_RIGHT_PAD, NEW_RIGHT_PAD, 1)
    print('OK: right column padding reduced')
else:
    errors.append('FAIL: right column padding not found')

# ── 3. Shrink stats row padding ───────────────────────────────────────────────
OLD_STATS = 'gap:3,padding:`10px 14px`},children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001f95a'
NEW_STATS = 'gap:2,padding:`8px 12px`},children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001f95a'
if OLD_STATS in content:
    content = content.replace(OLD_STATS, NEW_STATS, 1)
    print('OK: hatch date stats padding reduced')
else:
    errors.append('FAIL: stats hatch padding not found')

OLD_STATS2 = 'gap:3,padding:`10px 14px`},children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001fab1'
NEW_STATS2 = 'gap:2,padding:`8px 12px`},children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001fab1'
if OLD_STATS2 in content:
    content = content.replace(OLD_STATS2, NEW_STATS2, 1)
    print('OK: worm count stats padding reduced')
else:
    errors.append('FAIL: stats worm padding not found')

# ── 4. Purple accent Message button text ──────────────────────────────────────
OLD_MSG = "color:`#f8fafc`,fontWeight:700,fontSize:15,cursor:`pointer`},children:`Message`"
NEW_MSG = "color:`#c084fc`,fontWeight:700,fontSize:15,cursor:`pointer`},children:`Message`"
if OLD_MSG in content:
    content = content.replace(OLD_MSG, NEW_MSG, 1)
    print('OK: Message button text set to purple')
else:
    errors.append('FAIL: Message button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
