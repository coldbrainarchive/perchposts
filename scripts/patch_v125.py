#!/usr/bin/env python3
"""Patch v124 -> v125: whole nav pill turns red on notification instead of corner badge."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v124.js'
dst = '_deploy/assets/index-DUcNPOLc-v125.js'

content = open(src, encoding='utf-8').read()
errors = []

# 1. Modify Xn to treat color='#ef4444' as "notification red" → solid red pill, white text
OLD_XN = (
    'function Xn({record:e,name:t,color:n,onClick:r}){let i=Jn(e),a=e?.browser_id&&String(e.browser_id).startsWith(`bot-`),'
    'o=!a&&e?.is_admin===!0,s=!a&&!o&&e?.is_mod===!0,c=a?Yn[t]||`#94a3b8`:o?`#ffffff`:s?`#c084fc`:n||`#8fa0b6`;'
    'return(0,L.jsxs)(`span`,{className:`user-pill`,style:{color:(o||s)?`#0a0a0a`:c,'
    'background:o?`#ffffff`:s?`#c084fc`:`${c}18`,borderColor:o?`#ffffff`:s?`#c084fc`:`${c}55`,'
    'cursor:r?`pointer`:`default`},onClick:r,'
    'children:[i&&(0,L.jsx)(`span`,{className:`user-pill-badge`,children:i}),(0,L.jsx)(`span`,{className:`user-pill-name`,children:t})]})'
    '}'
)
NEW_XN = (
    'function Xn({record:e,name:t,color:n,onClick:r}){'
    'let i=Jn(e),a=e?.browser_id&&String(e.browser_id).startsWith(`bot-`),'
    'o=!a&&e?.is_admin===!0,s=!a&&!o&&e?.is_mod===!0,N=n===`#ef4444`,'
    'c=a?Yn[t]||`#94a3b8`:o?`#ffffff`:s?`#c084fc`:n||`#8fa0b6`;'
    'return(0,L.jsxs)(`span`,{className:`user-pill`,style:{'
    'color:(o||s)?`#0a0a0a`:N?`#ffffff`:c,'
    'background:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:`${c}18`,'
    'borderColor:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:`${c}55`,'
    'cursor:r?`pointer`:`default`},onClick:r,'
    'children:[i&&(0,L.jsx)(`span`,{className:`user-pill-badge`,children:i}),(0,L.jsx)(`span`,{className:`user-pill-name`,children:t})]})'
    '}'
)
if OLD_XN in content:
    content = content.replace(OLD_XN, NEW_XN, 1)
    print('OK: Xn updated — solid red pill when color=#ef4444')
else:
    errors.append('FAIL: Xn function not found')

# 2. Nav pill: pass color=#ef4444 when f>0, remove the corner badge span
OLD_NAV = (
    'className:`nav-user-pill`,style:{background:`none`,border:`none`,padding:0,cursor:`pointer`,display:`flex`},'
    'children:(()=>{let e=n===`admin`,t=n===`mod`,r=e||t?i:o||`Me`;'
    'return(0,L.jsx)(Xn,{record:{is_admin:e,is_mod:t&&!e,username:r,browser_id:Gn()},name:r,color:Hn(Gn(),r)})})()}),'
    'f>0&&(0,L.jsx)(`span`,{style:{position:`absolute`,top:-5,left:-5,background:`#ef4444`,color:`#fff`,'
    'fontSize:10,fontWeight:800,borderRadius:999,minWidth:16,height:16,display:`flex`,alignItems:`center`,'
    'justifyContent:`center`,padding:`0 3px`,pointerEvents:`none`,border:`1.5px solid #0f1117`,zIndex:10},'
    'children:f>99?`99+`:f})]'
)
NEW_NAV = (
    'className:`nav-user-pill`,style:{background:`none`,border:`none`,padding:0,cursor:`pointer`,display:`flex`},'
    'children:(()=>{let e=n===`admin`,t=n===`mod`,r=e||t?i:o||`Me`;'
    'return(0,L.jsx)(Xn,{record:{is_admin:e,is_mod:t&&!e,username:r,browser_id:Gn()},name:r,color:f>0?`#ef4444`:Hn(Gn(),r)})})()})]'
)
if OLD_NAV in content:
    content = content.replace(OLD_NAV, NEW_NAV, 1)
    print('OK: nav pill turns solid red on notification, badge removed')
else:
    errors.append('FAIL: nav pill badge block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
