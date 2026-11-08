#!/usr/bin/env python3
"""Patch v246 -> v247: redesign _UserCard to match profile card screenshot layout."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v246.js'
dst = '_deploy/assets/index-DUcNPOLc-v247.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Replace _UserCard component ───────────────────────────────────────────
OLD_CARD = (
    'function _UserCard({username:_un,onMessage:_om}){const[_s,_ss]=(0,_.useState)(null);'
    '(0,_.useEffect)(()=>{if(!_un)return;fetch(`${R}/user-stats?username=${encodeURIComponent(_un)}`)'
    '.then(r=>r.json()).then(d=>_ss(d)).catch(()=>{});},[_un]);if(!_s)return null;'
    'const _wc=_s.worm_count||0;const _rk=_RANKS.find(r=>_wc>=r.min&&_wc<=r.max);'
    'const _me=Qn()?.username;const _meta=(_rk?`${_rk.e} ${_rk.n} \xb7 `:``)+`\U0001fab1 ${_wc}`'
    '+(_s.joined_at?` \xb7 Joined ${Un(_s.joined_at)}`:``);\n'
    'return(0,L.jsxs)(`div`,{style:{padding:`12px 18px`,background:`#0f1117`,'
    'borderBottom:`1px solid #2e303a`,display:`flex`,alignItems:`center`,gap:12},'
    'children:[(0,L.jsxs)(`div`,{style:{flex:1},children:[(0,L.jsx)(`div`,{style:{color:`#f8fafc`,'
    'fontWeight:700,fontSize:15},children:_un}),(0,L.jsx)(`div`,{style:{color:`#64748b`,fontSize:12,'
    'marginTop:3},children:_meta})]}),_me&&_me!==_un&&(0,L.jsx)(`button`,{onClick:()=>_om(_un),'
    'style:{padding:`6px 16px`,borderRadius:10,border:`none`,background:`#c084fc`,color:`#14081d`,'
    'fontWeight:700,fontSize:12,cursor:`pointer`},children:`\U0001f4ac Message`})]});}'
)

NEW_CARD = (
    'function _UserCard({username:_un,onMessage:_om,record:_br}){'
    'const[_s,_ss]=(0,_.useState)(null);'
    '(0,_.useEffect)(()=>{'
    'if(!_un)return;'
    'fetch(`${R}/user-stats?username=${encodeURIComponent(_un)}`)'
    '.then(r=>r.json()).then(d=>_ss(d)).catch(()=>{});'
    '},[_un]);'
    'if(!_s)return null;'
    'const _wc=_s.worm_count||0;'
    'const _rk=_RANKS.find(r=>_wc>=r.min&&_wc<=r.max);'
    'const _me=Qn()?.username;'
    'const _bd=_br?Jn(_br):null;'
    'let _hd=`—`;'
    'if(_s.joined_at){const _d=new Date(_s.joined_at);'
    '_hd=String(_d.getDate()).padStart(2,`0`)+`-`+String(_d.getMonth()+1).padStart(2,`0`)+`-`+_d.getFullYear();}'
    'return(0,L.jsxs)(`div`,{style:{padding:`12px 16px`,borderBottom:`1px solid #2e303a`},'
    'children:['
    # Main card
    '(0,L.jsxs)(`div`,{style:{background:`#161920`,borderRadius:16,overflow:`hidden`,border:`1px solid #2e303a`},'
    'children:['
    # Top section
    '(0,L.jsxs)(`div`,{style:{display:`flex`,padding:`20px 20px 16px`},'
    'children:['
    # Left: bird + username
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,gap:10},'
    'children:['
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,fontSize:56,lineHeight:1},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display:`block`},'
    'children:_bd&&_bd.e?_bd.e:`\U0001f424`}),...(_bd&&_bd.s?_spEls(_bd.s,56):[])]}),'
    '(0,L.jsx)(`span`,{style:{background:`#c084fc`,color:`#14081d`,fontWeight:700,'
    'fontSize:12,padding:`3px 12px`,borderRadius:999,maxWidth:160,overflow:`hidden`,'
    'textOverflow:`ellipsis`,whiteSpace:`nowrap`},children:_un})]}),'
    # Vertical divider
    '(0,L.jsx)(`div`,{style:{width:1,background:`#2e303a`,margin:`0 8px`}}),'
    # Right: rank emoji + name
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,gap:8},'
    'children:['
    '(0,L.jsx)(`span`,{style:{fontSize:56,lineHeight:1},children:_rk?_rk.e:`\U0001f423`}),'
    '(0,L.jsx)(`span`,{style:{color:`#f8fafc`,fontWeight:600,fontSize:16,textAlign:`center`},'
    'children:_rk?_rk.n:`Hatchling`})]})]})'
    ','
    # Horizontal divider
    '(0,L.jsx)(`div`,{style:{height:1,background:`#2e303a`,margin:`0 20px`}}),'
    # Stats row
    '(0,L.jsxs)(`div`,{style:{display:`flex`,padding:`14px 20px`},'
    'children:['
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:4},'
    'children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001f95a Hatch Date`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:16,color:`#f1f5f9`,fontWeight:700},children:_hd})]}),'
    '(0,L.jsx)(`div`,{style:{width:1,background:`#2e303a`,margin:`0 16px`}}),'
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:4},'
    'children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001fab1 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:22,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
    ','
    # Message button (separate card below)
    '_me&&_me!==_un&&(0,L.jsx)(`button`,{onClick:()=>_om(_un),'
    'style:{width:`100%`,marginTop:10,padding:`14px`,borderRadius:16,'
    'border:`1px solid #2e303a`,background:`#161920`,'
    'color:`#f8fafc`,fontWeight:700,fontSize:16,cursor:`pointer`},'
    'children:`Message`})]});}'
)

if OLD_CARD in content:
    content = content.replace(OLD_CARD, NEW_CARD, 1)
    print('OK: _UserCard redesigned')
else:
    errors.append('FAIL: _UserCard not found')

# ── 2. Pass record:b[0]||null to _UserCard in Vr ─────────────────────────────
OLD_VR_CALL = 'p&&(0,L.jsx)(_UserCard,{username:p,onMessage:(_u)=>window.dispatchEvent(new CustomEvent(`open-dm`,{detail:_u}))})'
NEW_VR_CALL = 'p&&(0,L.jsx)(_UserCard,{username:p,record:b[0]||null,onMessage:(_u)=>window.dispatchEvent(new CustomEvent(`open-dm`,{detail:_u}))})'

if OLD_VR_CALL in content:
    content = content.replace(OLD_VR_CALL, NEW_VR_CALL, 1)
    print('OK: record prop passed to _UserCard')
else:
    errors.append('FAIL: _UserCard Vr call not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
