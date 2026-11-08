#!/usr/bin/env python3
"""Patch v173 -> v174: rename Account→Your Nest; collapsible password form."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v173.js'
dst = '_deploy/assets/index-DUcNPOLc-v174.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Rename Account tab to Your Nest ───────────────────────────────────────
old_count = content.count('label:`Account`')
content = content.replace('label:`Account`', 'label:`Your Nest`')
new_count = content.count('label:`Your Nest`')
if new_count == old_count and old_count > 0:
    print(f'OK: renamed Account → Your Nest ({new_count} occurrences)')
else:
    errors.append('FAIL: Account label not found or mismatch')

# ── 2. Add _pwOpen state variable ────────────────────────────────────────────
OLD_STATE = ',[_wc,_swc]=(0,_.useState)(0),[_hd,_shd]=(0,_.useState)(null),ee'
NEW_STATE = ',[_wc,_swc]=(0,_.useState)(0),[_hd,_shd]=(0,_.useState)(null),[_pwOpen,_setPwOpen]=(0,_.useState)(!1),ee'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: _pwOpen state added')
else:
    errors.append('FAIL: state declaration not found')

# ── 3. Make password form collapsible — same in BOTH O and D sections ─────────
# The password card appears twice (O and D sections). Replace both.
OLD_PW_CARD = (
    '(0,L.jsxs)(`div`,{className:`content-card`,style:{display:`flex`,flexDirection:`column`,gap:8},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`Change Password`}),'
    '(0,L.jsx)(`input`,{type:`password`,placeholder:`New password`,value:u,onChange:e=>d(e.target.value),onKeyDown:e=>e.key===`Enter`&&re(),style:{padding:`9px 12px`,borderRadius:10,border:`1px solid #3f4756`,background:`#0f1117`,color:`#f8fafc`,fontSize:16,width:`100%`,boxSizing:`border-box`}}),'
    '(0,L.jsx)(`button`,{onClick:re,style:{padding:`9px 14px`,borderRadius:10,border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:13,cursor:`pointer`},children:`Update Password`})'
    ']})'
)
NEW_PW_CARD = (
    # Collapsed: single button, same size as Log out
    '_pwOpen?'
    '(0,L.jsxs)(`div`,{className:`content-card`,style:{display:`flex`,flexDirection:`column`,gap:8},children:['
    '(0,L.jsx)(`input`,{type:`password`,placeholder:`New password`,value:u,onChange:e=>d(e.target.value),onKeyDown:e=>{if(e.key===`Enter`)re();if(e.key===`Escape`)_setPwOpen(!1)},autoFocus:!0,style:{padding:`9px 12px`,borderRadius:10,border:`1px solid #3f4756`,background:`#0f1117`,color:`#f8fafc`,fontSize:16,width:`100%`,boxSizing:`border-box`}}),'
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8},children:['
    '(0,L.jsx)(`button`,{onClick:re,style:{flex:1,padding:`10px 0`,borderRadius:12,border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,cursor:`pointer`},children:`Update Password`}),'
    '(0,L.jsx)(`button`,{onClick:()=>_setPwOpen(!1),style:{padding:`10px 14px`,borderRadius:12,border:`none`,background:`#1f2937`,color:`#94a3b8`,fontWeight:700,fontSize:14,cursor:`pointer`},children:`Cancel`})'
    ']})]}):'
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8},children:['
    '(0,L.jsx)(`button`,{onClick:()=>_setPwOpen(!0),style:{flex:1,padding:`12px 0`,borderRadius:12,border:`none`,background:`#1f2937`,color:`#c084fc`,fontWeight:700,fontSize:14,cursor:`pointer`},children:`Change password`})'
    ']})'
)

count = content.count(OLD_PW_CARD)
if count > 0:
    content = content.replace(OLD_PW_CARD, NEW_PW_CARD)
    print(f'OK: password form made collapsible ({count} section(s))')
else:
    errors.append('FAIL: password card not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
