#!/usr/bin/env python3
"""Patch v278 -> v280: move user results into Lr search dropdown.
Fixes step-ordering bug from v279 where step 4 removed the UR state just added
to Lr in step 1 (both used the same short pattern for replace-1st-match)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v278.js'
dst = '_deploy/assets/index-DUcNPOLc-v280.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove UR state from Vr FIRST (before adding to Lr, to avoid collision) ─
# Use surrounding context so we only hit Vr's instance
OLD_VR_UR_STATE = '[SRLoading,setSRLoading]=(0,_.useState)(!1),[UR,setUR]=(0,_.useState)([]),'
NEW_VR_UR_STATE = '[SRLoading,setSRLoading]=(0,_.useState)(!1),'
if OLD_VR_UR_STATE in content:
    content = content.replace(OLD_VR_UR_STATE, NEW_VR_UR_STATE, 1)
    print('OK: UR state removed from Vr')
else:
    errors.append('FAIL: Vr UR state (with context) not found')

# ── 2. Remove user fetch from Vr search useEffect ────────────────────────────
OLD_VR_FETCH = (
    'fetch(`${R}/search-users?q=${encodeURIComponent(m)}`)'
    '.then(_ur=>_ur.ok?_ur.json():{users:[]}).then(_ud=>setUR(_ud.users||[])).catch(()=>setUR([]));'
)
if OLD_VR_FETCH in content:
    content = content.replace(OLD_VR_FETCH, '', 1)
    print('OK: user fetch removed from Vr')
else:
    errors.append('FAIL: Vr user fetch not found')

# ── 3. Remove setUR([]) from Vr search early-return ──────────────────────────
OLD_VR_CLEAR = 'setSR(null);setSRLoading(!1);setUR([]);return'
NEW_VR_CLEAR = 'setSR(null);setSRLoading(!1);return'
if OLD_VR_CLEAR in content:
    content = content.replace(OLD_VR_CLEAR, NEW_VR_CLEAR, 1)
    print('OK: setUR([]) removed from Vr early return')
else:
    errors.append('FAIL: Vr early return not found')

# ── 4. Remove user cards section from Vr feed render ─────────────────────────
OLD_VR_RENDER = (
    'm&&UR.length>0&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:6,padding:`8px 12px`,background:`#161920`,borderRadius:12,border:`1px solid #2e303a`,marginBottom:8},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.06em`,marginBottom:4},children:`Users`}),'
    'UR.map(_ur=>(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:10,padding:`6px 8px`,borderRadius:8,cursor:`pointer`,background:`transparent`},'
    'onClick:()=>{window.location.href=`/?user=${encodeURIComponent(_ur.username)}`;},'
    'children:[(0,L.jsx)(Xn,{record:{username:_ur.username,is_admin:_ur.role===`admin`,is_mod:_ur.role===`mod`},name:_ur.username,color:Hn(null,_ur.username)}),]'
    '},_ur.username))]})'
    ','
)
if OLD_VR_RENDER in content:
    content = content.replace(OLD_VR_RENDER, '', 1)
    print('OK: user cards section removed from Vr feed')
else:
    errors.append('FAIL: Vr user render section not found')

# ── 5. Fix empty state: remove UR.length===0 condition ───────────────────────
OLD_EMPTY = 'm&&!SRLoading&&SR!==null&&b.length===0&&UR.length===0&&'
NEW_EMPTY = 'm&&!SRLoading&&SR!==null&&b.length===0&&'
if OLD_EMPTY in content:
    content = content.replace(OLD_EMPTY, NEW_EMPTY, 1)
    print('OK: empty state condition simplified')
else:
    print('NOTE: empty state already clean')

# ── 6. Add [UR,setUR] state to Lr (now safe — no Vr collision) ───────────────
OLD_LR_STATE = '[P,W]=(0,_.useState)(!1),c=(0,_.useRef)(null)'
NEW_LR_STATE = '[P,W]=(0,_.useState)(!1),[UR,setUR]=(0,_.useState)([]),c=(0,_.useRef)(null)'
if OLD_LR_STATE in content:
    content = content.replace(OLD_LR_STATE, NEW_LR_STATE, 1)
    print('OK: UR state added to Lr')
else:
    errors.append('FAIL: Lr state anchor not found')

# ── 7. Add user fetch to Lr debounce effect ───────────────────────────────────
OLD_DEBOUNCE = (
    'let e=setTimeout(()=>{let e=new URLSearchParams(u.current);'
    'n.trim()?e.set(`q`,n.trim()):e.delete(`q`),t(e,{replace:!0})},300);'
    'return()=>clearTimeout(e)},[n])'
)
NEW_DEBOUNCE = (
    'let e=setTimeout(()=>{let e=new URLSearchParams(u.current);'
    'n.trim()?e.set(`q`,n.trim()):e.delete(`q`),t(e,{replace:!0});'
    'n.trim()?fetch(`${R}/search-users?q=${encodeURIComponent(n.trim())}`)'
    '.then(_r=>_r.ok?_r.json():{users:[]}).then(_d=>setUR(_d.users||[])).catch(()=>setUR([])):setUR([]);'
    '},300);return()=>clearTimeout(e)},[n])'
)
if OLD_DEBOUNCE in content:
    content = content.replace(OLD_DEBOUNCE, NEW_DEBOUNCE, 1)
    print('OK: user fetch added to Lr debounce')
else:
    errors.append('FAIL: Lr debounce not found')

# ── 8. Add Users section to dropdown (after Countries) ────────────────────────
# Build closing sequences programmatically to avoid ]/) vs |/) typo confusion
_CLOSE_OLD = ']})' * 4 + '})' + '}' + 'function Rr'  # countries+outer+dropdown+bar-wrap+shell+body
_CLOSE_NEW = ']})' * 3 + '})' + '}' + 'function Rr'  # outer+dropdown+bar-wrap+shell+body (countries already in transition)

OLD_DROPDOWN_END = (
    'children:e.flag}),(0,L.jsx)(`span`,{className:`sugg-label`,children:e.name})]},e.name))'
) + _CLOSE_OLD

NEW_DROPDOWN_END = (
    'children:e.flag}),(0,L.jsx)(`span`,{className:`sugg-label`,children:e.name})]},e.name))]}),'
    'UR.length>0&&(0,L.jsxs)(L.Fragment,{children:['
    '(C||w||T)&&(0,L.jsx)(`div`,{className:`search-divider`}),'
    '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Users`}),'
    'UR.map(_u=>(0,L.jsxs)(`button`,{className:`search-suggestion`,type:`button`,'
    'onClick:()=>{a(!1);setUR([]);window.location.href=`/?user=${encodeURIComponent(_u.username)}`;},'
    'children:[(0,L.jsx)(`span`,{className:`sugg-icon`,children:(Jn({username:_u.username,browser_id:null})||{}).e||`🐦`}),'
    '(0,L.jsx)(`span`,{className:`sugg-label`,children:_u.username})]},_u.username))]}),'
) + _CLOSE_NEW

if OLD_DROPDOWN_END in content:
    content = content.replace(OLD_DROPDOWN_END, NEW_DROPDOWN_END, 1)
    print('OK: Users section added to dropdown')
else:
    errors.append('FAIL: dropdown end anchor not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
