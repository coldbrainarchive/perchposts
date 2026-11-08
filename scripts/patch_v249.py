#!/usr/bin/env python3
"""Patch v248 -> v249: _UserCard — username color matches tag color, two-column layout, compact."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v248.js'
dst = '_deploy/assets/index-DUcNPOLc-v249.js'

content = open(src, encoding='utf-8').read()
errors = []

old_start = content.find('function _UserCard(')
old_end   = content.find('\nfunction Vr(', old_start)
OLD_FULL  = content[old_start:old_end]

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
    'const _bd=_br?Jn(_br):(_un?Jn({username:_un,browser_id:`_`}):null);'
    # Color matching the user tag (same as Xn / postcard username color)
    'const _col=Hn(_br?.browser_id||`_`,_un);'
    'let _hd=`—`;'
    'if(_s.joined_at){const _d=new Date(_s.joined_at);'
    '_hd=String(_d.getDate()).padStart(2,`0`)+`-`+String(_d.getMonth()+1).padStart(2,`0`)+`-`+_d.getFullYear();}'
    'return(0,L.jsxs)(`div`,{style:{padding:`10px 14px`,borderBottom:`1px solid #2e303a`},'
    'children:['
    '(0,L.jsxs)(`div`,{style:{background:`#161920`,borderRadius:14,border:`1px solid #2e303a`,overflow:`hidden`},'
    'children:['
    # Top two-column section
    '(0,L.jsxs)(`div`,{style:{display:`flex`,minHeight:100},'
    'children:['
    # Left: bird + username pill
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,'
    'justifyContent:`center`,gap:8,padding:`14px 12px`},'
    'children:['
    '_bd&&_bd.hat?'
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,width:32,height:32,overflow:`visible`,flexShrink:0},'
    'children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,'
    'style:{position:`absolute`,height:54,width:`auto`,bottom:0,left:`50%`,transform:`translateX(-50%)`}})]}):'
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,fontSize:40,lineHeight:1},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display:`block`},'
    'children:_bd&&_bd.e?_bd.e:`\U0001f424`}),...(_bd&&_bd.s?_spEls(_bd.s,40):[])]}),'
    # Username pill — color matches their tag
    '(0,L.jsx)(`span`,{className:`user-pill`,'
    'style:{color:`#0a0a0a`,background:_col,borderColor:_col,cursor:`default`,'
    'maxWidth:150,overflow:`hidden`,textOverflow:`ellipsis`},'
    'children:_un})]}),'
    # Vertical divider
    '(0,L.jsx)(`div`,{style:{width:1,background:`#2e303a`,flexShrink:0}}),'
    # Right: rank label + rank pill
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,'
    'justifyContent:`center`,gap:8,padding:`14px 12px`},'
    'children:['
    '(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.06em`},children:`\U0001f947 Rank`}),'
    '_rk?(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:5,'
    'padding:`4px 12px`,borderRadius:999,border:`1px solid #a855f7`,'
    'background:`rgba(192,132,252,0.12)`,color:`#c084fc`,'
    'fontSize:13,fontWeight:700,whiteSpace:`nowrap`},'
    'children:[_rk.e,` `,_rk.n]}):null]})]}),'
    # Divider
    '(0,L.jsx)(`div`,{style:{height:1,background:`#2e303a`}}),'
    # Stats row
    '(0,L.jsxs)(`div`,{style:{display:`flex`},'
    'children:['
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3,padding:`10px 14px`},'
    'children:['
    '(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001f95a Hatch Date`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:14,color:`#f1f5f9`,fontWeight:700},children:_hd})]}),'
    '(0,L.jsx)(`div`,{style:{width:1,background:`#2e303a`}}),'
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3,padding:`10px 14px`},'
    'children:['
    '(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001fab1 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:18,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
    ','
    '_me&&_me!==_un&&(0,L.jsx)(`button`,{onClick:()=>_om(_un),'
    'style:{width:`100%`,marginTop:8,padding:`11px`,borderRadius:12,'
    'border:`1px solid #2e303a`,background:`#161920`,'
    'color:`#f8fafc`,fontWeight:700,fontSize:15,cursor:`pointer`},'
    'children:`Message`})]});}'
)

if OLD_FULL in content:
    content = content.replace(OLD_FULL, NEW_CARD, 1)
    print('OK: _UserCard updated with tag-matching color and two-column layout')
else:
    errors.append('FAIL: _UserCard not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
