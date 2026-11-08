#!/usr/bin/env python3
"""Patch v523 -> v524: Uniform centred 3-column layout for user card and Nest bottom row."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v523.js'
dst = '_deploy/assets/index-DUcNPOLc-v524.js'

content = open(src, encoding='utf-8').read()
errors = []

COL  = 'flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,gap:4,padding:`10px 8px`'
LBL  = 'fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`'
PILL = ('display:`inline-flex`,alignItems:`center`,height:20,padding:`0 8px`,'
        'borderRadius:999,border:`1px solid #a855f7`,'
        'background:`rgba(192,132,252,0.12)`,color:`#c084fc`,'
        'fontSize:11,fontWeight:700,whiteSpace:`nowrap`')

# ── 1. User card bottom row ───────────────────────────────────────────────────
OLD_CARD = (
    'display:`flex`,flexDirection:`column`,gap:2,padding:`8px 12px`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`🥚 Hatch Date`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:14,color:`#f1f5f9`,fontWeight:700},children:_hd})]})'
    ',(0,L.jsx)(`div`,{style:{width:1,background:`#2e303a`}}),'
    '_clan&&(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:2,padding:`8px 12px`,alignItems:`center`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`Clan`}),'
    '(0,L.jsx)(`span`,{style:{fontSize:20,lineHeight:1},children:_clan.e}),'
    '(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,height:20,padding:`0 8px`,borderRadius:999,border:`1px solid #a855f7`,background:`rgba(192,132,252,0.12)`,color:`#c084fc`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`},children:_clan.n})]}),'
    '_clan&&(0,L.jsx)(`div`,{style:{width:1,background:`#2e303a`}}),'
    '(0,L.jsxs)(`div`,{style:{flex:1,'
    'display:`flex`,flexDirection:`column`,gap:2,padding:`8px 12px`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`🪱 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:18,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
)
NEW_CARD = (
    COL + ',borderRight:`1px solid #2e303a`},'
    'children:[(0,L.jsx)(`div`,{style:{' + LBL + '},children:`🥚 Hatch Date`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_hd})]}),'
    '_clan&&(0,L.jsxs)(`div`,{style:{' + COL + ',borderRight:`1px solid #2e303a`},'
    'children:[(0,L.jsx)(`div`,{style:{' + LBL + '},children:`Clan`}),'
    '(0,L.jsx)(`span`,{style:{fontSize:18,lineHeight:1},children:_clan.e}),'
    '(0,L.jsx)(`span`,{style:{' + PILL + '},children:_clan.n})]}),'
    '(0,L.jsxs)(`div`,{style:{' + COL + '},'
    'children:[(0,L.jsx)(`div`,{style:{' + LBL + '},children:`🪱 Worms`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:18,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
)
if OLD_CARD in content:
    content = content.replace(OLD_CARD, NEW_CARD, 1)
    print('OK: user card bottom row unified')
else:
    errors.append('FAIL: user card bottom row not found')

# ── 2. Nest panel bottom row ──────────────────────────────────────────────────
COLN = 'flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,gap:4,padding:`12px 8px`'
LBLN = 'fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`'

OLD_NEST = (
    'display:`flex`,flexDirection:`column`,gap:3},children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`🥚 Hatch Date`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:14,color:`#f1f5f9`,fontWeight:600},children:_hd||`—`})]})'
    ',_clanN&&(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3,borderLeft:`1px solid #2e303a`,paddingLeft:16,alignItems:`center`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`Clan`}),'
    '(0,L.jsx)(`span`,{style:{fontSize:22,lineHeight:1},children:_clanN.e}),'
    '(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,height:20,padding:`0 8px`,borderRadius:999,border:`1px solid #a855f7`,background:`rgba(192,132,252,0.12)`,color:`#c084fc`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`},children:_clanN.n})]}),'
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3,borderLeft:`1px solid #2e303a`,paddingLeft:16},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`🪱 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:22,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
)
NEW_NEST = (
    COLN + ',borderRight:`1px solid #2e303a`},'
    'children:[(0,L.jsx)(`div`,{style:{' + LBLN + '},children:`🥚 Hatch Date`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_hd||`—`})]}),'
    '_clanN&&(0,L.jsxs)(`div`,{style:{' + COLN + ',borderRight:`1px solid #2e303a`},'
    'children:[(0,L.jsx)(`div`,{style:{' + LBLN + '},children:`Clan`}),'
    '(0,L.jsx)(`span`,{style:{fontSize:20,lineHeight:1},children:_clanN.e}),'
    '(0,L.jsx)(`span`,{style:{' + PILL + '},children:_clanN.n})]}),'
    '(0,L.jsxs)(`div`,{style:{' + COLN + '},'
    'children:[(0,L.jsx)(`div`,{style:{' + LBLN + '},children:`🪱 Worms`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:22,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
)
if OLD_NEST in content:
    content = content.replace(OLD_NEST, NEW_NEST, 1)
    print('OK: Nest bottom row unified')
else:
    errors.append('FAIL: Nest bottom row not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
