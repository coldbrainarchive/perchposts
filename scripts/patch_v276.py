#!/usr/bin/env python3
"""Patch v275 -> v276: search also queries registered users from mod_users via
/search-users, and shows matching user cards above post results so you can find
any registered user even if they haven't posted."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v275.js'
dst = '_deploy/assets/index-DUcNPOLc-v276.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add UR (user results) state next to SR/SRLoading ──────────────────────
OLD_STATE = '[SR,setSR]=(0,_.useState)(null),[SRLoading,setSRLoading]=(0,_.useState)(!1),'
NEW_STATE = '[SR,setSR]=(0,_.useState)(null),[SRLoading,setSRLoading]=(0,_.useState)(!1),[UR,setUR]=(0,_.useState)([]),'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: UR state added')
else:
    errors.append('FAIL: SR state not found')

# ── 2. Patch search useEffect to also fetch /search-users ────────────────────
OLD_SEARCH = (
    'if(!m){setSR(null);setSRLoading(!1);return}setSRLoading(!0);'
    'fetch(`${R}/get-posts?search=${encodeURIComponent(m)}&limit=1000`)'
)
NEW_SEARCH = (
    'if(!m){setSR(null);setSRLoading(!1);setUR([]);return}setSRLoading(!0);'
    'fetch(`${R}/search-users?q=${encodeURIComponent(m)}`)'
    '.then(_ur=>_ur.ok?_ur.json():{users:[]}).then(_ud=>setUR(_ud.users||[])).catch(()=>setUR([]));'
    'fetch(`${R}/get-posts?search=${encodeURIComponent(m)}&limit=1000`)'
)
if OLD_SEARCH in content:
    content = content.replace(OLD_SEARCH, NEW_SEARCH, 1)
    print('OK: search useEffect fetches /search-users')
else:
    errors.append('FAIL: search useEffect not found')

# ── 3. Render user result cards above post list in home feed ──────────────────
OLD_CHILDREN = 'children:[b.slice(0,o).map(e=>(0,L.jsx)(Ir,{post:e,commentCount:n[e.id]'
NEW_CHILDREN = (
    'children:['
    # User results section — shown when search is active and users were found
    'm&&UR.length>0&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:6,padding:`8px 12px`,background:`#161920`,borderRadius:12,border:`1px solid #2e303a`,marginBottom:8},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.06em`,marginBottom:4},children:`Users`}),'
    'UR.map(_ur=>(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:10,padding:`6px 8px`,borderRadius:8,cursor:`pointer`,background:`transparent`},'
    'onClick:()=>{window.location.href=`/?user=${encodeURIComponent(_ur.username)}`;},'
    'children:[(0,L.jsx)(Xn,{record:{username:_ur.username,is_admin:_ur.role===`admin`,is_mod:_ur.role===`mod`},name:_ur.username,color:Hn(null,_ur.username)}),'
    '_ur.role===`admin`&&(0,L.jsx)(`span`,{style:{fontSize:10,background:`#fff`,color:`#000`,borderRadius:4,padding:`1px 5px`,fontWeight:700},children:`admin`}),'
    '_ur.role===`mod`&&(0,L.jsx)(`span`,{style:{fontSize:10,background:`#c084fc`,color:`#14081d`,borderRadius:4,padding:`1px 5px`,fontWeight:700},children:`mod`})]'
    '},_ur.username))]})'
    ','
    'b.slice(0,o).map(e=>(0,L.jsx)(Ir,{post:e,commentCount:n[e.id]'
)
if OLD_CHILDREN in content:
    content = content.replace(OLD_CHILDREN, NEW_CHILDREN, 1)
    print('OK: user results rendered above post list')
else:
    errors.append('FAIL: home-feed children array not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
