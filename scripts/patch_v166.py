#!/usr/bin/env python3
"""Patch v165 -> v166: remove buttons from header, clean account tab bottom."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v165.js'
dst = '_deploy/assets/index-DUcNPOLc-v166.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove Logout + Change password buttons from header center column ──────
OLD_HDR_BTNS = (
    '(0,L.jsx)(Xn,{record:{is_admin:t===`admin`,is_mod:t===`mod`,username:te,browser_id:k},name:te,color:A}),'
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8},children:['
    '(0,L.jsx)(`button`,{onClick:()=>{o(),a()},style:{padding:`6px 14px`,borderRadius:999,border:`none`,background:`#7c3aed`,color:`#fff`,fontWeight:700,fontSize:12,cursor:`pointer`},children:`Logout`}),'
    'O&&(0,L.jsx)(`button`,{onClick:()=>l(`account`),style:{padding:`6px 14px`,borderRadius:999,border:`none`,background:`#7c3aed`,color:`#fff`,fontWeight:700,fontSize:12,cursor:`pointer`},children:`Change password`})'
    ']})]}):'
)
NEW_HDR_BTNS = (
    '(0,L.jsx)(Xn,{record:{is_admin:t===`admin`,is_mod:t===`mod`,username:te,browser_id:k},name:te,color:A})'
    ']})})'
    ':'
)
if OLD_HDR_BTNS in content:
    content = content.replace(OLD_HDR_BTNS, NEW_HDR_BTNS, 1)
    print('OK: buttons removed from header')
else:
    errors.append('FAIL: header buttons not found')

# ── 2. Remove username copy bubble from account tab ───────────────────────────
# Match from the content-card wrapping the username label to the end of that card
OLD_USERNAME_CARD = (
    'children:`Username`})'
    ',(0,L.jsxs)(`div`,{style:{padding:`9px 12px`,borderRadius:10,border:`1px solid #2e303a`,'
    'background:`#16171d`,color:`#94a3b8`,fontSize:14,display:`flex`,alignItems:`center`,'
    'justifyContent:`space-between`},children:[r||`—`,'
    'r&&(0,L.jsx)(`button`,{onClick:function(ev){'
    'try{navigator.clipboard.writeText(r);var b=ev.currentTarget;b.textContent="✓";'
    'b.style.color="#22c55e";setTimeout(function(){b.textContent="\U0001f4cb";b.style.color="#64748b"},1500)}'
    'catch(err){}},style:{background:`transparent`,border:`none`,cursor:`pointer`,'
    'color:`#64748b`,fontSize:15,padding:`0 2px`,lineHeight:1,flexShrink:0},'
    'children:`\U0001f4cb`})]})]})'
)
NEW_USERNAME_CARD = 'children:`Username`})]}'  # stub: keep the label div but remove the card
# Actually easier: remove the entire username content-card
# Let's find the outer content-card div for username and remove it entirely
idx_start = content.find('(0,L.jsxs)(`div`,{className:`content-card`,style:{display:`flex`,flexDirection:`column`,gap:8},children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`Username`})')
idx_end = content.find(',(0,L.jsxs)(`div`,{className:`content-card`,style:{display:`flex`,flexDirection:`column`,gap:8},children:[(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`Change Password`})', idx_start)
if idx_start >= 0 and idx_end >= 0:
    content = content[:idx_start] + content[idx_end+1:]  # remove username card + leading comma
    print('OK: username copy bubble removed')
else:
    errors.append(f'FAIL: username card not found (start={idx_start}, end={idx_end})')

# ── 3. Replace ghost 🚪 Log out button with clean button row at bottom ────────
OLD_LOGOUT = (
    '(0,L.jsx)(`button`,{onClick:()=>{o(),a()},style:{padding:`10px 16px`,borderRadius:12,'
    'border:`1px solid #374151`,background:`transparent`,color:`#94a3b8`,fontWeight:700,'
    'fontSize:14,cursor:`pointer`},children:`\U0001f6aa Log out`})'
)
NEW_LOGOUT = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8,marginTop:4},children:['
    '(0,L.jsx)(`button`,{onClick:()=>{o(),a()},style:{flex:1,padding:`12px 0`,'
    'borderRadius:12,border:`none`,background:`#1f2937`,color:`#f87171`,'
    'fontWeight:700,fontSize:14,cursor:`pointer`},children:`Log out`})'
    ']})'
)
if OLD_LOGOUT in content:
    content = content.replace(OLD_LOGOUT, NEW_LOGOUT, 1)
    print('OK: logout button replaced with clean styled button')
else:
    errors.append('FAIL: logout button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
