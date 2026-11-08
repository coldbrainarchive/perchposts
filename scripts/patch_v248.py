#!/usr/bin/env python3
"""Patch v247 -> v248: _UserCard — bird+username matches Kr panel, rank as purple pill, compact."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v247.js'
dst = '_deploy/assets/index-DUcNPOLc-v248.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_CARD = 'function _UserCard({username:_un,onMessage:_om,record:_br}){'
# Get full old card
old_start = content.find(OLD_CARD)
old_end = content.find('\nfunction Vr(', old_start)
OLD_FULL = content[old_start:old_end]

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
    # Use Jn with the record (same as Kr uses Jn({username,browser_id}))
    'const _bd=_br?Jn(_br):(_un?Jn({username:_un,browser_id:`_`}):null);'
    'let _hd=`—`;'
    'if(_s.joined_at){const _d=new Date(_s.joined_at);'
    '_hd=String(_d.getDate()).padStart(2,`0`)+`-`+String(_d.getMonth()+1).padStart(2,`0`)+`-`+_d.getFullYear();}'
    'return(0,L.jsxs)(`div`,{style:{padding:`12px 16px`,borderBottom:`1px solid #2e303a`},'
    'children:['
    # Main card
    '(0,L.jsxs)(`div`,{style:{background:`#161920`,borderRadius:16,border:`1px solid #2e303a`,overflow:`hidden`},'
    'children:['
    # Top row: bird + username pill + rank pill
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:10,padding:`14px 16px`},'
    'children:['
    # Bird (40px, same style as Kr)
    '_bd&&_bd.hat?'
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,width:30,height:30,overflow:`visible`,flexShrink:0},'
    'children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,'
    'style:{position:`absolute`,height:52,width:`auto`,bottom:0,left:`50%`,transform:`translateX(-50%)`}})]}):'
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,fontSize:40,lineHeight:1,flexShrink:0},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display:`block`},'
    'children:_bd&&_bd.e?_bd.e:`\U0001f424`}),...(_bd&&_bd.s?_spEls(_bd.s,40):[])]}),'
    # Username pill (user-pill class, purple like mod)
    '(0,L.jsx)(`span`,{className:`user-pill`,'
    'style:{color:`#0a0a0a`,background:`#c084fc`,borderColor:`#a855f7`,cursor:`default`,'
    'maxWidth:160,overflow:`hidden`,textOverflow:`ellipsis`},'
    'children:_un}),'
    # Rank pill (purple accent)
    '_rk&&(0,L.jsx)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4,'
    'height:22,padding:`0 9px`,borderRadius:999,border:`1px solid #a855f7`,'
    'background:`rgba(192,132,252,0.15)`,color:`#c084fc`,'
    'fontSize:12,fontWeight:700,whiteSpace:`nowrap`,flexShrink:0},'
    'children:[_rk.e,` `,_rk.n]})]}),'
    # Divider
    '(0,L.jsx)(`div`,{style:{height:1,background:`#2e303a`,margin:`0 16px`}}),'
    # Stats row
    '(0,L.jsxs)(`div`,{style:{display:`flex`,padding:`12px 16px`},'
    'children:['
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3},'
    'children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001f95a Hatch Date`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:14,color:`#f1f5f9`,fontWeight:600},children:_hd})]}),'
    '(0,L.jsx)(`div`,{style:{width:1,background:`#2e303a`,margin:`0 12px`}}),'
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3},'
    'children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,'
    'textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001fab1 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:18,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]})'
    ','
    # Message button
    '_me&&_me!==_un&&(0,L.jsx)(`button`,{onClick:()=>_om(_un),'
    'style:{width:`100%`,marginTop:8,padding:`12px`,borderRadius:14,'
    'border:`1px solid #2e303a`,background:`#161920`,'
    'color:`#f8fafc`,fontWeight:700,fontSize:15,cursor:`pointer`},'
    'children:`Message`})]});}'
)

if OLD_FULL in content:
    content = content.replace(OLD_FULL, NEW_CARD, 1)
    print('OK: _UserCard redesigned with Kr-style bird + pills')
else:
    errors.append('FAIL: _UserCard full body not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
