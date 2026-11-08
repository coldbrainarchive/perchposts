#!/usr/bin/env python3
"""Patch v251 -> v252: inbox rows — use Xn (postcard username badge) instead of manual bird+pill."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v251.js'
dst = '_deploy/assets/index-DUcNPOLc-v252.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_ROW = (
    '_dmConvs.map((_cv,_ci)=>{const _cbd=Jn({username:_cv.contact,browser_id:null});'
    'const _ccol=Hn(null,_cv.contact);'
    'return(0,L.jsxs)(`div`,{onClick:()=>{_setDmThread(_cv.contact);_setDmMsgs([]);},'
    'style:{display:`flex`,alignItems:`center`,gap:8,padding:`10px 14px`,'
    'borderBottom:`1px solid #1a1c23`,cursor:`pointer`},'
    'children:['
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,fontSize:22,lineHeight:1,flexShrink:0},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_cbd&&_cbd.f?_cbd.f:``,display:`block`},'
    'children:_cbd&&_cbd.e?_cbd.e:`\U0001f424`}),...(_cbd&&_cbd.s?_spEls(_cbd.s,22):[])]}),'
    '(0,L.jsx)(`span`,{className:`user-pill`,'
    'style:{color:`#0a0a0a`,background:_ccol,borderColor:_ccol,cursor:`default`,flexShrink:0},'
    'children:_cv.contact}),'
    '_cv.unread>0&&(0,L.jsx)(`span`,{style:{background:`#c084fc`,color:`#14081d`,'
    'borderRadius:999,fontSize:10,fontWeight:700,padding:`1px 6px`,flexShrink:0},'
    'children:_cv.unread}),'
    '(0,L.jsx)(`span`,{style:{color:`#475569`,fontSize:12,flex:1,overflow:`hidden`,'
    'textOverflow:`ellipsis`,whiteSpace:`nowrap`,minWidth:0},'
    'children:_cv.last_content||``}),'
    '(0,L.jsx)(`span`,{style:{color:`#374151`,fontSize:11,flexShrink:0},'
    'children:Un(_cv.last_at)})]},_ci);}'
    ')'
)

NEW_ROW = (
    '_dmConvs.map((_cv,_ci)=>'
    '(0,L.jsxs)(`div`,{onClick:()=>{_setDmThread(_cv.contact);_setDmMsgs([]);},'
    'style:{display:`flex`,alignItems:`center`,gap:8,padding:`10px 14px`,'
    'borderBottom:`1px solid #1a1c23`,cursor:`pointer`},'
    'children:['
    # Xn postcard badge — same as postcard username tag
    '(0,L.jsx)(Xn,{record:{username:_cv.contact},name:_cv.contact,'
    'color:Hn(null,_cv.contact)}),'
    # Unread badge
    '_cv.unread>0&&(0,L.jsx)(`span`,{style:{background:`#c084fc`,color:`#14081d`,'
    'borderRadius:999,fontSize:10,fontWeight:700,padding:`1px 6px`,flexShrink:0},'
    'children:_cv.unread}),'
    # Message preview
    '(0,L.jsx)(`span`,{style:{color:`#475569`,fontSize:12,flex:1,overflow:`hidden`,'
    'textOverflow:`ellipsis`,whiteSpace:`nowrap`,minWidth:0},'
    'children:_cv.last_content||``}),'
    # Time
    '(0,L.jsx)(`span`,{style:{color:`#374151`,fontSize:11,flexShrink:0},'
    'children:Un(_cv.last_at)})]},_ci))'
    ')'
)

if OLD_ROW in content:
    content = content.replace(OLD_ROW, NEW_ROW, 1)
    print('OK: inbox rows now use Xn postcard badge')
else:
    errors.append('FAIL: conversation row not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
