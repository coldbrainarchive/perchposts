#!/usr/bin/env python3
"""Patch v357 -> v358:
- Fix toggle width (was stretching full width) + remove emoji from HUDDLE label
- Redesign member picker: chips live inside search bar (like main feed), 16px input prevents iOS zoom
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v357.js'
dst = '_deploy/assets/index-DUcNPOLc-v358.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Fix toggle: remove emoji, add width:fit-content so it doesn't stretch ──
OLD_TOGGLE = (
    '(0,L.jsxs)(`div`,{className:`sort-toggle`,style:{marginBottom:10,alignSelf:`flex-start`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn`:`sort-toggle-btn active`,'
    'onClick:()=>{_setIsHuddle(!1);_setHmTagged([]);_setHmTagQ(``);},'
    'children:`POST`}),'
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn active`:`sort-toggle-btn`,'
    'onClick:()=>{_setIsHuddle(!0);},'
    'children:`\U0001f465 HUDDLE`})'
    ']})'
)
NEW_TOGGLE = (
    '(0,L.jsxs)(`div`,{className:`sort-toggle`,style:{marginBottom:10,width:`fit-content`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn`:`sort-toggle-btn active`,'
    'onClick:()=>{_setIsHuddle(!1);_setHmTagged([]);_setHmTagQ(``);},'
    'children:`POST`}),'
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn active`:`sort-toggle-btn`,'
    'onClick:()=>{_setIsHuddle(!0);},'
    'children:`HUDDLE`})'
    ']})'
)
if OLD_TOGGLE in content:
    content = content.replace(OLD_TOGGLE, NEW_TOGGLE, 1)
    print('OK: toggle fixed (width:fit-content, no emoji)')
else:
    errors.append('FAIL: toggle not found')

# ── 2. Replace the full member picker with search-bar style ───────────────────
# Old: outer div > label + chips row + search input row + results dropdown
# New: label + search-bar (chips + input inside) + results dropdown below

OLD_PICKER = (
    '_isHuddle&&(0,L.jsxs)(`div`,{style:{marginTop:6},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:12,color:`#94a3b8`,marginBottom:6},'
    'children:`Add the users you want in this huddle:`}),'
    '_hmTagged.length>0&&(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:4,marginBottom:6},'
    'children:_hmTagged.map(_u=>(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'gap:4,position:`relative`},'
    'children:['
)

# Find the full block from the OLD_PICKER start to the closing of the member picker section
idx = content.find('_isHuddle&&(0,L.jsxs)(`div`,{style:{marginTop:6},children:[')
if idx == -1:
    errors.append('FAIL: member picker start not found')
else:
    # Find the end - the textarea that follows
    end_marker = '!_isHuddle&&(0,L.jsx)(`textarea`,'
    end_idx = content.find(end_marker, idx)
    if end_idx == -1:
        errors.append('FAIL: member picker end not found')
    else:
        old_picker_full = content[idx:end_idx]

        # Build user pill JSX helper
        def user_pill(uname='_u.username', bid='_u.browser_id||null'):
            return (
                '(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4,height:22,'
                'padding:`0 7px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,'
                f'background:Hn({bid},{uname}),'
                'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,'
                'lineHeight:1,flexShrink:0,boxSizing:`border-box`},'
                f'children:[(0,L.jsx)(`span`,{{children:(Jn({{username:{uname},browser_id:{bid}}})||{{}}).e||`\U0001f426`}}),'
                f'(0,L.jsx)(`span`,{{children:{uname}}})'
                ']})'
            )

        new_picker = (
            # Outer container
            '_isHuddle&&(0,L.jsxs)(`div`,{style:{marginTop:6},children:['
            '(0,L.jsx)(`div`,{style:{fontSize:12,color:`#94a3b8`,marginBottom:6},'
            'children:`Add the users you want in this huddle:`}),'
            # search-bar contains chips + input inline
            '(0,L.jsxs)(`div`,{className:`search-bar`,children:['
            # chips inside bar
            '..._hmTagged.map(_u=>(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:2,position:`relative`},'
            'children:['
            + user_pill() + ','
            '(0,L.jsx)(`button`,{type:`button`,'
            'onClick:()=>_setHmTagged(_hmTagged.filter(_t=>_t.username!==_u.username)),'
            'style:{position:`absolute`,top:-4,right:-4,background:`#374151`,border:`none`,'
            'color:`#fff`,borderRadius:999,width:14,height:14,cursor:`pointer`,'
            'fontSize:9,display:`flex`,alignItems:`center`,justifyContent:`center`,lineHeight:1},'
            'children:`\xd7`})'
            ']},_u.username)),'
            # input inside bar (16px prevents iOS zoom)
            '(0,L.jsx)(`input`,{className:`search-input`,value:_hmTagQ,'
            'onChange:e=>{_setHmTagQ(e.target.value);clearTimeout(_hmTimer.current);'
            '_hmTimer.current=setTimeout(()=>{'
            'if(e.target.value.trim()){fetch(`${R}/search-users?q=${encodeURIComponent(e.target.value.trim())}`)'
            '.then(_r=>_r.ok?_r.json():{users:[]})'
            '.then(_d=>_setHmTagR(_d.users||[]))'
            '.catch(()=>_setHmTagR([]));}else{_setHmTagR([]);}},300);},'
            'placeholder:`+ User`})'
            ']})'  # close search-bar
            ','
            # results dropdown
            '_hmTagR.length>0&&(0,L.jsx)(`div`,{style:{marginTop:4,maxHeight:160,overflowY:`auto`,'
            'borderRadius:8,border:`1px solid #374151`,background:`#0f1117`},'
            'children:_hmTagR.filter(_u=>!_hmTagged.find(_t=>_t.username===_u.username)).slice(0,8)'
            '.map(_u=>(0,L.jsx)(`button`,{type:`button`,'
            'onClick:()=>{_setHmTagged([..._hmTagged,_u]);_setHmTagQ(``);_setHmTagR([]);},'
            'style:{display:`flex`,padding:`6px 10px`,border:`none`,background:`none`,cursor:`pointer`},'
            'children:' + user_pill() +
            '},_u.username))})'
            ']})'  # close outer div
            ','
        )

        content = content[:idx] + new_picker + content[end_idx:]
        print('OK: member picker redesigned as search-bar style with chips inside')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
