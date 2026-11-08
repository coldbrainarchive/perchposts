#!/usr/bin/env python3
"""Patch v348 -> v349:
- Add search input to board/country picker in new post form
- Add user tagging section (search + chips) to new post form
- Include tagged_users in post submission
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v348.js'
dst = '_deploy/assets/index-DUcNPOLc-v349.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add new state variables ────────────────────────────────────────────────
OLD_STATE = '[ne,re]=(0,_.useState)(!1),ie=(0,_.useRef)(null),j=(0,_.useRef)(null)'
NEW_STATE = (
    '[ne,re]=(0,_.useState)(!1),'
    '[_npSrch,_setNpSrch]=(0,_.useState)(``),'
    '[_npTagQ,_setNpTagQ]=(0,_.useState)(``),'
    '[_npTagR,_setNpTagR]=(0,_.useState)([]),'
    '[_npTagged,_setNpTagged]=(0,_.useState)([]),'
    '_npTimer=(0,_.useRef)(null),'
    'ie=(0,_.useRef)(null),j=(0,_.useRef)(null)'
)
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: state variables added')
else:
    errors.append('FAIL: state chain end not found')

# ── 2. Add search input between header and two-column picker ──────────────────
OLD_PICKER_HDR = (
    'children:`Select board & country`})]}),(0,L.jsxs)(`div`,{style:{display:`flex`,minHeight:0},'
)
NEW_PICKER_HDR = (
    'children:`Select board & country`})]})'
    ',(0,L.jsx)(`div`,{style:{padding:`4px 10px 6px`,borderBottom:`1px solid #2a2d38`},'
    'children:(0,L.jsx)(`input`,{value:_npSrch,onChange:e=>_setNpSrch(e.target.value),'
    'placeholder:`Search boards or regions…`,'
    'style:{width:`100%`,boxSizing:`border-box`,padding:`4px 8px`,borderRadius:6,'
    'border:`1px solid #374151`,background:`#1a1d28`,color:`#e2e8f0`,fontSize:11,outline:`none`}})})'
    ',(0,L.jsxs)(`div`,{style:{display:`flex`,minHeight:0},'
)
if OLD_PICKER_HDR in content:
    content = content.replace(OLD_PICKER_HDR, NEW_PICKER_HDR, 1)
    print('OK: search input added to picker')
else:
    errors.append('FAIL: picker header not found')

# ── 3. Filter boards by search ────────────────────────────────────────────────
OLD_BOARD_FILTER = 'nr.filter(e=>!e.virtual).map('
NEW_BOARD_FILTER = 'nr.filter(e=>!e.virtual&&(!_npSrch||e.name.toLowerCase().includes(_npSrch.toLowerCase())||e.slug.toLowerCase().includes(_npSrch.toLowerCase()))).map('
if OLD_BOARD_FILTER in content:
    content = content.replace(OLD_BOARD_FILTER, NEW_BOARD_FILTER, 1)
    print('OK: board list filtered by search')
else:
    errors.append('FAIL: board filter not found')

# ── 4. Filter regions by search ───────────────────────────────────────────────
OLD_REGION_FILTER = 'rr.filter(e=>e!==`World`).map('
NEW_REGION_FILTER = 'rr.filter(e=>e!==`World`&&(!_npSrch||e.toLowerCase().includes(_npSrch.toLowerCase()))).map('
if OLD_REGION_FILTER in content:
    content = content.replace(OLD_REGION_FILTER, NEW_REGION_FILTER, 1)
    print('OK: region list filtered by search')
else:
    errors.append('FAIL: region filter not found')

# ── 5. Filter countries in drilldown by search ────────────────────────────────
OLD_COUNTRY_FILTER = 'or.filter(e=>ar[e.name]===S).map('
NEW_COUNTRY_FILTER = 'or.filter(e=>ar[e.name]===S&&(!_npSrch||e.name.toLowerCase().includes(_npSrch.toLowerCase()))).map('
if OLD_COUNTRY_FILTER in content:
    content = content.replace(OLD_COUNTRY_FILTER, NEW_COUNTRY_FILTER, 1)
    print('OK: country drilldown filtered by search')
else:
    errors.append('FAIL: country drilldown filter not found')

# ── 6. Add user tagging section after picker, before feed-post-time ───────────
OLD_AFTER_PICKER = (
    ']},e))]})})]})]})]})]}),(0,L.jsx)(`span`,{className:`feed-post-time`,children:`now`})'
)
NEW_AFTER_PICKER = (
    ']},e))]})})]})]})]})]})'
    ',(0,L.jsxs)(`div`,{style:{borderTop:`1px solid #2a2d38`,padding:`8px 12px`},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:10,fontWeight:700,color:`#4b5563`,textTransform:`uppercase`,'
    'letterSpacing:`0.08em`,marginBottom:6},children:`Tag Users`}),'
    '_npTagged.length>0&&(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:4,marginBottom:6},'
    'children:_npTagged.map(_u=>(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'gap:4,padding:`2px 6px`,borderRadius:999,background:`rgba(168,85,247,0.15)`,'
    'border:`1px solid rgba(168,85,247,0.3)`,fontSize:11,color:`#c084fc`},'
    'children:[`@`,_u.username,'
    '(0,L.jsx)(`button`,{type:`button`,'
    'onClick:()=>_setNpTagged(_npTagged.filter(_t=>_t.username!==_u.username)),'
    'style:{background:`none`,border:`none`,color:`#c084fc`,cursor:`pointer`,padding:`0 0 0 2px`,fontSize:11},'
    'children:`\xd7`})]},_u.username))}),'
    '(0,L.jsx)(`input`,{value:_npTagQ,'
    'onChange:e=>{_setNpTagQ(e.target.value);clearTimeout(_npTimer.current);'
    '_npTimer.current=setTimeout(()=>{'
    'if(e.target.value.trim()){fetch(`${R}/search-users?q=${encodeURIComponent(e.target.value.trim())}`)'
    '.then(_r=>_r.ok?_r.json():{users:[]})'
    '.then(_d=>_setNpTagR(_d.users||[]))'
    '.catch(()=>_setNpTagR([]));}else{_setNpTagR([]);}},300);},'
    'placeholder:`Search users to tag…`,'
    'style:{width:`100%`,boxSizing:`border-box`,padding:`4px 8px`,borderRadius:6,'
    'border:`1px solid #374151`,background:`#1a1d28`,color:`#e2e8f0`,fontSize:11,outline:`none`}}),'
    '_npTagR.length>0&&(0,L.jsx)(`div`,{style:{marginTop:4,maxHeight:120,overflowY:`auto`,'
    'borderRadius:6,border:`1px solid #374151`},'
    'children:_npTagR.filter(_u=>!_npTagged.find(_t=>_t.username===_u.username)).slice(0,8)'
    '.map(_u=>(0,L.jsx)(`button`,{type:`button`,'
    'onClick:()=>{_setNpTagged([..._npTagged,_u]);_setNpTagQ(``);_setNpTagR([]);},'
    'style:{display:`block`,width:`100%`,padding:`6px 10px`,border:`none`,'
    'background:`none`,color:`#e2e8f0`,fontSize:12,textAlign:`left`,cursor:`pointer`},'
    'children:`@${_u.username}`},_u.username))})'
    ']})'
    ',(0,L.jsx)(`span`,{className:`feed-post-time`,children:`now`})'
)
if OLD_AFTER_PICKER in content:
    content = content.replace(OLD_AFTER_PICKER, NEW_AFTER_PICKER, 1)
    print('OK: user tagging section added')
else:
    errors.append('FAIL: picker closing / feed-post-time anchor not found')

# ── 7. Include tagged_users in post submission ────────────────────────────────
OLD_SUBMIT = 'browser_id:f,...t}'
NEW_SUBMIT = 'browser_id:f,tagged_users:_npTagged.map(_u=>_u.username),...t}'
if OLD_SUBMIT in content:
    content = content.replace(OLD_SUBMIT, NEW_SUBMIT, 1)
    print('OK: tagged_users added to submission')
else:
    errors.append('FAIL: submission body not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
