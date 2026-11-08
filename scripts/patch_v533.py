#!/usr/bin/env python3
"""Patch v532 -> v533: Shift HATCHED divider left by giving it flex:0.85 vs 1 for others."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v532.js'
dst = '_deploy/assets/index-DUcNPOLc-v533.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── Nest: HATCHED column gets flex:0.85 (divider shifts left) ────────────────
# The HATCHED column is the first child — it has borderRight and comes before _clanN&&
OLD_NEST_HD = ('flex:1,minWidth:0,display:`flex`,flexDirection:`column`,'
               'justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`,'
               'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
               'fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
               'letterSpacing:`0.05em`,textAlign:`center`,width:`100%`},children:`🥚 Hatched`})')
NEW_NEST_HD = ('flex:0.85,minWidth:0,display:`flex`,flexDirection:`column`,'
               'justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`,'
               'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
               'fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
               'letterSpacing:`0.05em`,textAlign:`center`,width:`100%`},children:`🥚 Hatched`})')
if OLD_NEST_HD in content:
    content = content.replace(OLD_NEST_HD, NEW_NEST_HD, 1)
    print('OK: Nest HATCHED column flex:0.85')
else:
    errors.append('FAIL: Nest HATCHED column not found')

# ── User card: same fix ───────────────────────────────────────────────────────
OLD_CARD_HD = ('flex:1,minWidth:0,display:`flex`,flexDirection:`column`,'
               'justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`,'
               'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
               'fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
               'letterSpacing:`0.05em`},children:`🥚 Hatched`})')
NEW_CARD_HD = ('flex:0.85,minWidth:0,display:`flex`,flexDirection:`column`,'
               'justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`,'
               'borderRight:`1px solid #2e303a`},children:[(0,L.jsx)(`div`,{style:{'
               'fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
               'letterSpacing:`0.05em`},children:`🥚 Hatched`})')
if OLD_CARD_HD in content:
    content = content.replace(OLD_CARD_HD, NEW_CARD_HD, 1)
    print('OK: user card HATCHED column flex:0.85')
else:
    errors.append('FAIL: user card HATCHED column not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
