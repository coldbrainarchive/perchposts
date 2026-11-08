#!/usr/bin/env python3
"""Patch v358 -> v359:
- Move POST/HUDDLE toggle into the nav row (replace "New post" text)
- Show static HUDDLES board pill in card header when in huddle mode
- Change placeholder from "+ User" to "Add User"
- Hide Link/Photo/Video buttons when in huddle mode
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v358.js'
dst = '_deploy/assets/index-DUcNPOLc-v359.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Move toggle into nav row (replace "New post" text) ─────────────────────
OLD_NAV = (
    'children:`←`}),(0,L.jsx)(`span`,{style:{fontSize:13,fontWeight:600,color:`#94a3b8`},'
    'children:`New post`})]}),(0,L.jsxs)(`div`,{className:`sort-toggle`,'
    'style:{marginBottom:10,width:`fit-content`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn`:`sort-toggle-btn active`,'
    'onClick:()=>{_setIsHuddle(!1);_setHmTagged([]);_setHmTagQ(``);},'
    'children:`POST`}),'
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn active`:`sort-toggle-btn`,'
    'onClick:()=>{_setIsHuddle(!0);},'
    'children:`HUDDLE`})'
    ']})'
)
NEW_NAV = (
    'children:`←`}),'
    # Toggle replaces "New post" — sits right after the back arrow
    '(0,L.jsxs)(`div`,{className:`sort-toggle`,style:{width:`fit-content`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn`:`sort-toggle-btn active`,'
    'onClick:()=>{_setIsHuddle(!1);_setHmTagged([]);_setHmTagQ(``);},'
    'children:`POST`}),'
    '(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn active`:`sort-toggle-btn`,'
    'onClick:()=>{_setIsHuddle(!0);},'
    'children:`HUDDLE`})'
    ']})'
    ']})'  # closes nav row
)
if OLD_NAV in content:
    content = content.replace(OLD_NAV, NEW_NAV, 1)
    print('OK: toggle moved into nav row')
else:
    errors.append('FAIL: nav row + toggle not found')

# ── 2. Show HUDDLES pill in card header when in huddle mode ───────────────────
# Currently the feed-post-header is hidden (display:none) when _isHuddle
# Replace with conditional: show static huddle header OR board picker header
OLD_HDR = 'className:`feed-post-header`,style:{display:_isHuddle?`none`:``},children:'
NEW_HDR = (
    'className:`feed-post-header`,'
    'children:_isHuddle?'
    # Huddle mode: static HUDDLES pill + "now"
    '(0,L.jsxs)(`div`,{className:`feed-post-board-row`,children:['
    '(0,L.jsx)(`span`,{className:`feed-post-board-group`,children:'
    '(0,L.jsx)(Ar,{boardName:`Huddles`,small:!1})'
    '}),'
    '(0,L.jsx)(`span`,{className:`feed-post-time`,style:{marginLeft:`auto`},children:`now`})'
    ']})'
    ':'
)
if OLD_HDR in content:
    content = content.replace(OLD_HDR, NEW_HDR, 1)
    print('OK: static HUDDLES pill shown in card header')
else:
    errors.append('FAIL: feed-post-header not found')

# ── 3. Change "+ User" placeholder to "Add User" ─────────────────────────────
OLD_PH = 'placeholder:`+ User`})'
NEW_PH = 'placeholder:`Add User`})'
if OLD_PH in content:
    content = content.replace(OLD_PH, NEW_PH, 1)
    print('OK: placeholder changed to "Add User"')
else:
    errors.append('FAIL: placeholder not found')

# ── 4. Hide Link/Photo/Video buttons when in huddle mode ─────────────────────
OLD_LINK = (
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>D(`link`),className:`feed-post-action-pill`,'
    'children:`🔗 Link`}),(0,L.jsx)(`button`,{type:`button`,onClick:()=>ie.current?.click(),'
    'disabled:ne,className:`feed-post-action-pill`,children:ne?`…`:`🖼 Photo`}),'
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>j.current?.click(),'
    'disabled:ne,className:`feed-post-action-pill`,children:ne?`…`:`🎥 Video`})'
)
NEW_LINK = (
    '!_isHuddle&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>D(`link`),className:`feed-post-action-pill`,'
    'children:`🔗 Link`}),!_isHuddle&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>ie.current?.click(),'
    'disabled:ne,className:`feed-post-action-pill`,children:ne?`…`:`🖼 Photo`}),'
    '!_isHuddle&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>j.current?.click(),'
    'disabled:ne,className:`feed-post-action-pill`,children:ne?`…`:`🎥 Video`})'
)
if OLD_LINK in content:
    content = content.replace(OLD_LINK, NEW_LINK, 1)
    print('OK: Link/Photo/Video hidden in huddle mode')
else:
    errors.append('FAIL: Link/Photo/Video buttons not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
