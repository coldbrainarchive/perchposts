#!/usr/bin/env python3
"""Patch v356 -> v357:
- POST/HUDDLE toggle uses sort-toggle segmented pill style
- Huddle user search results use proper user pill tags (same as feed filter)
- Tagged member chips use proper user pill tags
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v356.js'
dst = '_deploy/assets/index-DUcNPOLc-v357.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Replace POST/HUDDLE toggle with sort-toggle style ──────────────────────
OLD_TOGGLE = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:6,padding:`4px 0 10px`},children:['
    '(0,L.jsx)(`button`,{type:`button`,'
    'onClick:()=>{_setIsHuddle(!1);_setHmTagged([]);_setHmTagQ(``);},'
    'style:{padding:`4px 12px`,borderRadius:999,border:`1px solid rgba(148,163,184,0.3)`,'
    'background:_isHuddle?`transparent`:`#a855f7`,color:_isHuddle?`#94a3b8`:`#fff`,'
    'fontSize:12,fontWeight:700,cursor:`pointer`,letterSpacing:`0.04em`},'
    'children:`POST`}),'
    '(0,L.jsx)(`button`,{type:`button`,'
    'onClick:()=>{_setIsHuddle(!0);},'
    'style:{padding:`4px 12px`,borderRadius:999,border:`1px solid rgba(148,163,184,0.3)`,'
    'background:_isHuddle?`#a855f7`:`transparent`,color:_isHuddle?`#fff`:`#94a3b8`,'
    'fontSize:12,fontWeight:700,cursor:`pointer`,letterSpacing:`0.04em`},'
    'children:`\U0001f465 HUDDLE`})'
    ']})'
)
NEW_TOGGLE = (
    '(0,L.jsxs)(`div`,{className:`sort-toggle`,style:{marginBottom:10,alignSelf:`flex-start`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn`:`sort-toggle-btn active`,'
    'onClick:()=>{_setIsHuddle(!1);_setHmTagged([]);_setHmTagQ(``);},'
    'children:`POST`}),'
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn active`:`sort-toggle-btn`,'
    'onClick:()=>{_setIsHuddle(!0);},'
    'children:`\U0001f465 HUDDLE`})'
    ']})'
)
if OLD_TOGGLE in content:
    content = content.replace(OLD_TOGGLE, NEW_TOGGLE, 1)
    print('OK: toggle changed to sort-toggle style')
else:
    errors.append('FAIL: toggle not found')

# Helper: user pill JSX (same pattern as feed filter Users section)
def user_pill_jsx(username_expr, browser_id_expr='null'):
    return (
        '(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4,height:22,'
        'padding:`0 7px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,'
        f'background:Hn({browser_id_expr},{username_expr}),'
        'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,'
        'lineHeight:1,flexShrink:0,boxSizing:`border-box`},'
        f'children:[(0,L.jsx)(`span`,'
        f'{{children:(Jn({{username:{username_expr},browser_id:{browser_id_expr}}})||{{}}).e||`\U0001f426`}}),'
        f'(0,L.jsx)(`span`,{{children:{username_expr}}})'
        ']})'
    )

# ── 2. Replace tagged member chips with user pills ────────────────────────────
OLD_CHIPS = (
    '_hmTagged.map(_u=>(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'gap:4,padding:`2px 8px`,borderRadius:999,background:`rgba(168,85,247,0.15)`,'
    'border:`1px solid rgba(168,85,247,0.4)`,fontSize:12,color:`#c084fc`},'
    'children:[`@`,_u.username,'
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>_setHmTagged(_hmTagged.filter(_t=>_t.username!==_u.username)),'
    'style:{background:`none`,border:`none`,color:`#c084fc`,cursor:`pointer`,padding:`0 0 0 2px`,fontSize:11},'
    'children:`\xd7`})]},_u.username))'
)
NEW_CHIPS = (
    '_hmTagged.map(_u=>(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'gap:4,position:`relative`},'
    'children:['
    + user_pill_jsx('_u.username', '_u.browser_id||null') +
    ','
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>_setHmTagged(_hmTagged.filter(_t=>_t.username!==_u.username)),'
    'style:{position:`absolute`,top:-4,right:-4,background:`#374151`,border:`none`,'
    'color:`#fff`,borderRadius:999,width:14,height:14,cursor:`pointer`,'
    'fontSize:9,display:`flex`,alignItems:`center`,justifyContent:`center`,lineHeight:1},'
    'children:`\xd7`})'
    ']},_u.username))'
)
if OLD_CHIPS in content:
    content = content.replace(OLD_CHIPS, NEW_CHIPS, 1)
    print('OK: tagged member chips use user pill style')
else:
    errors.append('FAIL: tagged member chips not found')

# ── 3. Replace search result items with user pill style ───────────────────────
OLD_RESULTS = (
    '_hmTagR.filter(_u=>!_hmTagged.find(_t=>_t.username===_u.username)).slice(0,8)'
    '.map(_u=>(0,L.jsx)(`button`,{type:`button`,'
    'onClick:()=>{_setHmTagged([..._hmTagged,_u]);_setHmTagQ(``);_setHmTagR([]);},'
    'style:{display:`block`,width:`100%`,padding:`6px 10px`,border:`none`,'
    'background:`none`,color:`#e2e8f0`,fontSize:13,textAlign:`left`,cursor:`pointer`},'
    'children:`@${_u.username}`},_u.username))'
)
NEW_RESULTS = (
    '_hmTagR.filter(_u=>!_hmTagged.find(_t=>_t.username===_u.username)).slice(0,8)'
    '.map(_u=>(0,L.jsx)(`button`,{type:`button`,'
    'onClick:()=>{_setHmTagged([..._hmTagged,_u]);_setHmTagQ(``);_setHmTagR([]);},'
    'style:{display:`flex`,padding:`6px 10px`,border:`none`,'
    'background:`none`,cursor:`pointer`},'
    'children:' + user_pill_jsx('_u.username', '_u.browser_id||null') +
    '},_u.username))'
)
if OLD_RESULTS in content:
    content = content.replace(OLD_RESULTS, NEW_RESULTS, 1)
    print('OK: search results use user pill style')
else:
    errors.append('FAIL: search results not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
