#!/usr/bin/env python3
"""Patch v163 -> v164: clean header (bird+username+buttons only), rank/stats into account tab."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v163.js'
dst = '_deploy/assets/index-DUcNPOLc-v164.js'

content = open(src, encoding='utf-8').read()
errors = []

BTN = '{padding:`6px 14px`,borderRadius:999,border:`none`,background:`#7c3aed`,color:`#fff`,fontWeight:700,fontSize:12,cursor:`pointer`}'

# ── 1. Replace cluttered 3-col header with clean centred header ───────────────
OLD_HEADER = (
    'padding:`16px 18px`,borderBottom:`1px solid #2e303a`,position:`relative`},'
    'children:[e?(0,L.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:`1fr auto 1fr`,'
    'gap:10,alignItems:`flex-start`},children:['
    # left rank col
    '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:3},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:26,lineHeight:1},children:_rank.e}),'
    '(0,L.jsx)(`div`,{style:{fontWeight:700,fontSize:11,color:`#f1f5f9`,marginTop:4},children:_rank.n}),'
    '(0,L.jsx)(`div`,{style:{fontSize:10,color:`#64748b`,fontStyle:`italic`,lineHeight:1.4,marginTop:2},children:_rank.d})]}),'
    # centre col
    '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,alignItems:`center`,gap:7},children:['
    '(0,L.jsx)(`span`,{style:{fontSize:52,lineHeight:1,filter:_bird&&_bird.f?_bird.f:``,display:`block`},children:_bird&&_bird.e?_bird.e:`\U0001f424`}),'
    '(0,L.jsx)(Xn,{record:{is_admin:t===`admin`,is_mod:t===`mod`,username:te,browser_id:k},name:te,color:A}),'
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:5,marginTop:2},children:['
    '(0,L.jsx)(`button`,{onClick:()=>{o(),a()},style:{padding:`5px 12px`,borderRadius:999,border:`none`,background:`#7c3aed`,color:`#fff`,fontWeight:700,fontSize:11,cursor:`pointer`},children:`Logout`}),'
    'O&&(0,L.jsx)(`button`,{onClick:()=>l(`account`),style:{padding:`5px 12px`,borderRadius:999,border:`none`,background:`#7c3aed`,color:`#fff`,fontWeight:700,fontSize:11,cursor:`pointer`},children:`Change password`})'
    ']})]}),'
    # right stats col
    '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:10,alignItems:`flex-end`},children:['
    '(0,L.jsxs)(`div`,{style:{textAlign:`right`},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#94a3b8`},children:`\U0001f424 Hatch date`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:12,color:`#f1f5f9`,marginTop:3},children:_hd||`—`})]}),'
    '(0,L.jsxs)(`div`,{style:{textAlign:`right`},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#94a3b8`},children:`\U0001fab1 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:20,fontWeight:700,color:`#f1f5f9`,marginTop:3},children:_wc})]})]})]}):'
    'null,'
)

NEW_HEADER = (
    'padding:`20px 18px 16px`,borderBottom:`1px solid #2e303a`,position:`relative`},'
    'children:[e?(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,alignItems:`center`,gap:10},children:['
    '(0,L.jsx)(`span`,{style:{fontSize:56,lineHeight:1,filter:_bird&&_bird.f?_bird.f:``,display:`block`},children:_bird&&_bird.e?_bird.e:`\U0001f424`}),'
    '(0,L.jsx)(Xn,{record:{is_admin:t===`admin`,is_mod:t===`mod`,username:te,browser_id:k},name:te,color:A}),'
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8},children:['
    '(0,L.jsx)(`button`,{onClick:()=>{o(),a()},style:' + BTN + ',children:`Logout`}),'
    'O&&(0,L.jsx)(`button`,{onClick:()=>l(`account`),style:' + BTN + ',children:`Change password`})'
    ']})]):'
    'null,'
)

if OLD_HEADER in content:
    content = content.replace(OLD_HEADER, NEW_HEADER, 1)
    print('OK: header simplified')
else:
    errors.append('FAIL: old header not found')

# ── 2. Add rank card + stats to top of account tab (before the O&& username card) ──
OLD_ACCOUNT = 'c===`account`&&(0,L.jsxs)(`div`,{style:{padding:20,display:`flex`,flexDirection:`column`,gap:14},children:[O&&'
NEW_ACCOUNT = (
    'c===`account`&&(0,L.jsxs)(`div`,{style:{padding:20,display:`flex`,flexDirection:`column`,gap:14},children:['
    # Rank card (show for all logged-in users O or D)
    '(e&&!D)?(0,L.jsxs)(`div`,{className:`content-card`,style:{display:`flex`,flexDirection:`column`,gap:10},children:['
    # Rank row
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:10},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:36,lineHeight:1},children:_rank.e}),'
    '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:2},children:['
    '(0,L.jsx)(`div`,{style:{fontWeight:700,fontSize:15,color:`#f1f5f9`},children:_rank.n}),'
    '(0,L.jsx)(`div`,{style:{fontSize:12,color:`#64748b`,fontStyle:`italic`,lineHeight:1.4},children:_rank.d})]})]}),'
    # Stats row: hatch date + worm count
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:0,borderTop:`1px solid #2e303a`,paddingTop:10},children:['
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001f95a Hatch Date`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:14,color:`#f1f5f9`,fontWeight:600},children:_hd||`—`})]}),'
    '(0,L.jsxs)(`div`,{style:{flex:1,display:`flex`,flexDirection:`column`,gap:3,borderLeft:`1px solid #2e303a`,paddingLeft:16},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#64748b`,textTransform:`uppercase`,letterSpacing:`0.05em`},children:`\U0001fab1 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:22,color:`#f1f5f9`,fontWeight:700},children:_wc})]})]})]}):'
    'null,'
    'O&&'
)

if OLD_ACCOUNT in content:
    content = content.replace(OLD_ACCOUNT, NEW_ACCOUNT, 1)
    print('OK: rank + stats card added to account tab')
else:
    errors.append('FAIL: account tab start not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
