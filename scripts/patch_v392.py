#!/usr/bin/env python3
"""Patch v391 -> v392:
- Huddle tagged user chips: replace span+overlay-× pattern with tappable button chip
  (tap the pill itself to remove, same UX as main search bar chips)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v391.js'
dst = '_deploy/assets/index-DUcNPOLc-v392.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:2,position:`relative`},'
    'children:[(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4,height:22,'
    'padding:`0 7px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,'
    'background:_u.role===`admin`?`#ffffff`:Hn(_u.browser_id||null,_u.username),'
    'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1,flexShrink:0,boxSizing:`border-box`},'
    'children:[(()=>{const _jd=Jn({username:_u.username,browser_id:_u.browser_id||null,is_admin:_u.role===`admin`})||{};'
    'return typeof _jd===`object`&&_jd.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{height:13,width:13,objectFit:`contain`}}):'
    '(0,L.jsx)(`span`,{style:_jd.f?{filter:_jd.f}:{},children:_jd.e||`\U0001f426`});})() '
    ',(0,L.jsx)(`span`,{children:_u.username})]})'
    ',(0,L.jsx)(`button`,{type:`button`,onClick:()=>_setHmTagged(_hmTagged.filter(_t=>_t.username!==_u.username)),'
    'style:{position:`absolute`,top:-4,right:-4,background:`#374151`,border:`none`,color:`#fff`,borderRadius:999,'
    'width:14,height:14,cursor:`pointer`,fontSize:9,display:`flex`,alignItems:`center`,justifyContent:`center`,lineHeight:1},'
    'children:`×`})]},_u.username)'
)
NEW = (
    '(0,L.jsxs)(`button`,{type:`button`,className:`search-chip`,'
    'onClick:e=>{e.stopPropagation();_setHmTagged(_hmTagged.filter(_t=>_t.username!==_u.username));},'
    'style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},'
    'children:(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4,height:22,'
    'padding:`0 7px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,'
    'background:_u.role===`admin`?`#ffffff`:Hn(_u.browser_id||null,_u.username),'
    'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1,flexShrink:0,boxSizing:`border-box`},'
    'children:[(()=>{const _jd=Jn({username:_u.username,browser_id:_u.browser_id||null,is_admin:_u.role===`admin`})||{};'
    'return typeof _jd===`object`&&_jd.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{height:13,width:13,objectFit:`contain`}}):'
    '(0,L.jsx)(`span`,{style:_jd.f?{filter:_jd.f}:{},children:_jd.e||`\U0001f426`});})() '
    ',(0,L.jsx)(`span`,{children:_u.username})]})},_u.username)'
)

if OLD in content:
    # Verify brackets
    for label, s in [('OLD', OLD), ('NEW', NEW)]:
        p = s.count('(') - s.count(')')
        b = s.count('{') - s.count('}')
        if p != 0 or b != 0:
            errors.append(f'{label} unbalanced: p={p}, b={b}')
    if not errors:
        content = content.replace(OLD, NEW, 1)
        print('OK: tagged chips now tappable to remove (no × overlay)')
else:
    errors.append('FAIL: tagged chip span not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
