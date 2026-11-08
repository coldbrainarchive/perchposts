#!/usr/bin/env python3
"""Patch v522 -> v523: Add bird clans (Puffer's/Pecker's/Percher's) to user card and Nest."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v522.js'
dst = '_deploy/assets/index-DUcNPOLc-v523.js'

content = open(src, encoding='utf-8').read()
errors = []

CLAN_CONST = ('var _CLANS={"\U0001f424":"Pecker\'s","\U0001f426":"Percher\'s","\U0001f427":"Puffer\'s"};'
              'function _getClan(_b){if(!_b)return null;if(_b.hat)return{e:"\U0001f426",n:"Percher\'s"};'
              'var _n=_CLANS[_b.e];return _n?{e:_b.e,n:_n}:null;}')

# ── 1. Inject _CLANS constant before Xn component ────────────────────────────
OLD_XN = 'function Xn({'
if OLD_XN in content:
    content = content.replace(OLD_XN, CLAN_CONST + OLD_XN, 1)
    print('OK: _CLANS constant injected')
else:
    errors.append('FAIL: Xn function not found')

# ── 2. User card: derive _clan after _bd, insert between hatch/worm columns ──
OLD_BD = ('const _bd=_br?Jn(_br):(_un?Jn({username:_un,browser_id:`_`}):null);')
NEW_BD = ('const _bd=_br?Jn(_br):(_un?Jn({username:_un,browser_id:`_`}):null);'
          'const _clan=_getClan(_bd);')
if OLD_BD in content:
    content = content.replace(OLD_BD, NEW_BD, 1)
    print('OK: _clan derived in user card')
else:
    errors.append('FAIL: _bd declaration in user card not found')

# Insert clan column between hatch date and worm count in user card
OLD_CARD_ROW = (
    '(0,L.jsx)(`div`,{style:{width:1,background:`#2e303a`}}),'
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:2,padding:`8px 12px`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
    'letterSpacing:`0.05em`},children:`🪱 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:18,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
)
NEW_CARD_ROW = (
    '(0,L.jsx)(`div`,{style:{width:1,background:`#2e303a`}}),'
    '_clan&&(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:2,padding:`8px 12px`,alignItems:`center`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
    'letterSpacing:`0.05em`},children:`Clan`}),'
    '(0,L.jsx)(`span`,{style:{fontSize:20,lineHeight:1},children:_clan.e}),'
    '(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,height:20,padding:`0 8px`,'
    'borderRadius:999,border:`1px solid #a855f7`,background:`rgba(192,132,252,0.12)`,'
    'color:`#c084fc`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`},children:_clan.n})]}),'
    '_clan&&(0,L.jsx)(`div`,{style:{width:1,background:`#2e303a`}}),'
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:2,padding:`8px 12px`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
    'letterSpacing:`0.05em`},children:`🪱 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:18,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
)
if OLD_CARD_ROW in content:
    content = content.replace(OLD_CARD_ROW, NEW_CARD_ROW, 1)
    print('OK: clan column added to user card')
else:
    errors.append('FAIL: user card hatch/worm row not found')

# ── 3. Nest panel: derive _clan after _bird, insert between hatch/worm ────────
OLD_BIRD = ('let _bird=te?Jn({username:te,browser_id:k,is_admin:t===`admin`,is_mod:t===`mod`}):null;')
NEW_BIRD = ('let _bird=te?Jn({username:te,browser_id:k,is_admin:t===`admin`,is_mod:t===`mod`}):null;'
            'let _clanN=_getClan(_bird);')
if OLD_BIRD in content:
    content = content.replace(OLD_BIRD, NEW_BIRD, 1)
    print('OK: _clanN derived in Nest panel')
else:
    errors.append('FAIL: _bird declaration in Nest not found')

# Insert clan column between hatch date and worm count in Nest panel
OLD_NEST_ROW = (
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3,'
    'borderLeft:`1px solid #2e303a`,paddingLeft:16},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
    'letterSpacing:`0.05em`},children:`🪱 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:22,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
)
NEW_NEST_ROW = (
    '_clanN&&(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3,'
    'borderLeft:`1px solid #2e303a`,paddingLeft:16,alignItems:`center`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
    'letterSpacing:`0.05em`},children:`Clan`}),'
    '(0,L.jsx)(`span`,{style:{fontSize:22,lineHeight:1},children:_clanN.e}),'
    '(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,height:20,padding:`0 8px`,'
    'borderRadius:999,border:`1px solid #a855f7`,background:`rgba(192,132,252,0.12)`,'
    'color:`#c084fc`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`},children:_clanN.n})]}),'
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3,'
    'borderLeft:`1px solid #2e303a`,paddingLeft:16},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,'
    'letterSpacing:`0.05em`},children:`🪱 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:22,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
)
if OLD_NEST_ROW in content:
    content = content.replace(OLD_NEST_ROW, NEW_NEST_ROW, 1)
    print('OK: clan column added to Nest panel')
else:
    errors.append('FAIL: Nest panel hatch/worm row not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
