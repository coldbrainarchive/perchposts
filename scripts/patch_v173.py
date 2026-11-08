#!/usr/bin/env python3
"""Patch v172 -> v173: remove emoji from header pill; admin account tab matches regular layout."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v172.js'
dst = '_deploy/assets/index-DUcNPOLc-v173.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Replace Xn in header with a plain name-only pill ───────────────────────
OLD_HDR_XN = (
    '(0,L.jsx)(Xn,{record:{is_admin:t===`admin`,is_mod:t===`mod`,'
    'username:te,browser_id:k},name:te,color:A})]}):null'
)
NEW_HDR_XN = (
    '(0,L.jsx)(`span`,{className:`user-pill`,'
    'style:{color:`#0a0a0a`,background:A,borderColor:A,cursor:`default`},'
    'children:te})]}):null'
)
if OLD_HDR_XN in content:
    content = content.replace(OLD_HDR_XN, NEW_HDR_XN, 1)
    print('OK: header pill shows name only (no emoji)')
else:
    errors.append('FAIL: header Xn not found')

# ── 2. Replace D (admin/mod) account section ──────────────────────────────────
OLD_D_SECTION = (
    'D&&(0,L.jsxs)(L.Fragment,{children:['
    '(0,L.jsxs)(`div`,{className:`content-card`,style:{display:`flex`,flexDirection:`column`,gap:8},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`Username`}),'
    '(0,L.jsxs)(`div`,{style:{padding:`9px 12px`,borderRadius:10,border:`1px solid #2e303a`,background:`#16171d`,color:`#94a3b8`,fontSize:14},children:[`@`,n]})]}),'
    '(0,L.jsx)(I,{to:`/mod`,onClick:a,style:{display:`block`,padding:`10px 16px`,borderRadius:12,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,cursor:`pointer`,textDecoration:`none`,textAlign:`center`},children:`Open Mod Panel`}),'
    '(0,L.jsx)(`button`,{onClick:()=>{o(),a()},style:{padding:`10px 16px`,borderRadius:12,border:`1px solid #374151`,background:`transparent`,color:`#94a3b8`,fontWeight:700,fontSize:14,cursor:`pointer`},children:`🚪 Log out`})'
    ']})'
)
NEW_D_SECTION = (
    'D&&(0,L.jsxs)(L.Fragment,{children:['
    '(0,L.jsxs)(`div`,{className:`content-card`,style:{display:`flex`,flexDirection:`column`,gap:8},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`Change Password`}),'
    '(0,L.jsx)(`input`,{type:`password`,placeholder:`New password`,value:u,onChange:e=>d(e.target.value),onKeyDown:e=>e.key===`Enter`&&re(),style:{padding:`9px 12px`,borderRadius:10,border:`1px solid #3f4756`,background:`#0f1117`,color:`#f8fafc`,fontSize:16,width:`100%`,boxSizing:`border-box`}}),'
    '(0,L.jsx)(`button`,{onClick:re,style:{padding:`9px 14px`,borderRadius:10,border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:13,cursor:`pointer`},children:`Update Password`})'
    ']}),'
    '(0,L.jsx)(I,{to:`/mod`,onClick:a,style:{display:`block`,padding:`12px 0`,borderRadius:12,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,cursor:`pointer`,textDecoration:`none`,textAlign:`center`},children:`Open Mod Panel`}),'
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8,marginTop:4},children:['
    '(0,L.jsx)(`button`,{onClick:()=>{o(),a()},style:{flex:1,padding:`12px 0`,borderRadius:12,border:`none`,background:`#1f2937`,color:`#f87171`,fontWeight:700,fontSize:14,cursor:`pointer`},children:`Log out`})'
    ']})'
    ']})'
)
if OLD_D_SECTION in content:
    content = content.replace(OLD_D_SECTION, NEW_D_SECTION, 1)
    print('OK: admin account tab matches regular user layout')
else:
    errors.append('FAIL: D section not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
