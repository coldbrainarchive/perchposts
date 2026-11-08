#!/usr/bin/env python3
"""Patch v525 -> v526:
- Hatch Date -> Hatched
- Clan column: label = emoji + CLAN, value = PUFFER/PECKER/PERCHER (no apostrophe, big white text)
- Matches Hatched / Worms layout exactly
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v525.js'
dst = '_deploy/assets/index-DUcNPOLc-v526.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Fix _CLANS constant: remove apostrophes ────────────────────────────────
OLD_CLANS = ('var _CLANS={"\U0001f424":"Pecker\'s","\U0001f426":"Percher\'s","\U0001f427":"Puffer\'s"};'
             'function _getClan(_b){if(!_b)return null;if(_b.hat)return{e:"\U0001f426",n:"Percher\'s"};'
             'var _n=_CLANS[_b.e];return _n?{e:_b.e,n:_n}:null;}')
NEW_CLANS = ('var _CLANS={"\U0001f424":"Pecker","\U0001f426":"Percher","\U0001f427":"Puffer"};'
             'function _getClan(_b){if(!_b)return null;if(_b.hat)return{e:"\U0001f426",n:"Percher"};'
             'var _n=_CLANS[_b.e];return _n?{e:_b.e,n:_n}:null;}')
if OLD_CLANS in content:
    content = content.replace(OLD_CLANS, NEW_CLANS, 1)
    print('OK: clan apostrophes removed')
else:
    errors.append('FAIL: _CLANS constant not found')

# ── 2. User card: Hatch Date -> Hatched ──────────────────────────────────────
OLD_HD_C = 'children:`🥚 Hatch Date`}),(0,L.jsx)(`div`,{style:{fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_hd})]}),'
NEW_HD_C = 'children:`🥚 Hatched`}),(0,L.jsx)(`div`,{style:{fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_hd})]}),'
if OLD_HD_C in content:
    content = content.replace(OLD_HD_C, NEW_HD_C, 1)
    print('OK: user card Hatch Date -> Hatched')
else:
    errors.append('FAIL: user card Hatch Date label not found')

# ── 3. User card: replace clan emoji+pill with label+value layout ─────────────
OLD_CLAN_C = ('children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`Clan`}),'
              '(0,L.jsx)(`span`,{style:{fontSize:18,lineHeight:1},children:_clan.e}),'
              '(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,height:20,padding:`0 8px`,borderRadius:999,border:`1px solid #a855f7`,background:`rgba(192,132,252,0.12)`,color:`#c084fc`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`},children:_clan.n})]}),'
              '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,gap:4,padding:`10px 8px`},'
              'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`🪱 Worms`})')
NEW_CLAN_C = ('children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:_clan.e+` Clan`}),'
              '(0,L.jsx)(`div`,{style:{fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_clan.n.toUpperCase()})]}),'
              '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,gap:4,padding:`10px 8px`},'
              'children:[(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`🪱 Worms`})')
if OLD_CLAN_C in content:
    content = content.replace(OLD_CLAN_C, NEW_CLAN_C, 1)
    print('OK: user card clan column redesigned')
else:
    errors.append('FAIL: user card clan column not found')

# ── 4. Nest: Hatch Date -> Hatched ───────────────────────────────────────────
OLD_HD_N = 'children:`🥚 Hatch Date`}),(0,L.jsx)(`div`,{style:{fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_hd||`—`})]}),'
NEW_HD_N = 'children:`🥚 Hatched`}),(0,L.jsx)(`div`,{style:{fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_hd||`—`})]}),'
if OLD_HD_N in content:
    content = content.replace(OLD_HD_N, NEW_HD_N, 1)
    print('OK: Nest Hatch Date -> Hatched')
else:
    errors.append('FAIL: Nest Hatch Date label not found')

# ── 5. Nest: replace clan emoji+pill with label+value layout ──────────────────
OLD_CLAN_N = ('children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`Clan`}),'
              '(0,L.jsx)(`span`,{style:{fontSize:20,lineHeight:1},children:_clanN.e}),'
              '(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,height:20,padding:`0 8px`,borderRadius:999,border:`1px solid #a855f7`,background:`rgba(192,132,252,0.12)`,color:`#c084fc`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`},children:_clanN.n})]}),'
              '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,gap:4,padding:`12px 8px`},'
              'children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`🪱 Worms`})')
NEW_CLAN_N = ('children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:_clanN.e+` Clan`}),'
              '(0,L.jsx)(`div`,{style:{fontSize:15,color:`#f1f5f9`,fontWeight:700},children:_clanN.n.toUpperCase()})]}),'
              '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,justifyContent:`center`,gap:4,padding:`12px 8px`},'
              'children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`🪱 Worms`})')
if OLD_CLAN_N in content:
    content = content.replace(OLD_CLAN_N, NEW_CLAN_N, 1)
    print('OK: Nest clan column redesigned')
else:
    errors.append('FAIL: Nest clan column not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
