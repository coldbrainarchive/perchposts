#!/usr/bin/env python3
"""Patch v179 -> v180: smaller admin header bird; reorder + restyle mod panel btn."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v179.js'
dst = '_deploy/assets/index-DUcNPOLc-v180.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Slightly smaller header bird ──────────────────────────────────────────
OLD_HDR = (
    'width:`44px`,height:`44px`,overflow:`visible`},children:['
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{'
    'position:`absolute`,height:`76px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})'
    ']})'
)
NEW_HDR = (
    'width:`40px`,height:`40px`,overflow:`visible`},children:['
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{'
    'position:`absolute`,height:`68px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})'
    ']})'
)
if OLD_HDR in content:
    content = content.replace(OLD_HDR, NEW_HDR, 1)
    print('OK: header bird slightly smaller')
else:
    errors.append('FAIL: header bird not found')

# ── 2. Reorder D section: logout first, then mod panel below (same style) ────
OLD_ORDER = (
    '(0,L.jsx)(I,{to:`/mod`,onClick:a,'
    'style:{display:`block`,padding:`12px 0`,borderRadius:12,'
    'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,'
    'cursor:`pointer`,textDecoration:`none`,textAlign:`center`},'
    'children:`Open Mod Panel`}),'
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8,marginTop:4},children:['
    '(0,L.jsx)(`button`,{onClick:()=>{o(),a()},style:{flex:1,padding:`12px 0`,'
    'borderRadius:12,border:`none`,background:`#1f2937`,color:`#f87171`,'
    'fontWeight:700,fontSize:14,cursor:`pointer`},children:`Log out`})'
    ']})'
)
NEW_ORDER = (
    # Logout first (same style)
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8},children:['
    '(0,L.jsx)(`button`,{onClick:()=>{o(),a()},style:{flex:1,padding:`12px 0`,'
    'borderRadius:12,border:`none`,background:`#1f2937`,color:`#f87171`,'
    'fontWeight:700,fontSize:14,cursor:`pointer`},children:`Log out`})'
    ']}),'
    # Open Mod Panel below, same size/shape as logout but purple
    '(0,L.jsx)(I,{to:`/mod`,onClick:a,'
    'style:{display:`block`,padding:`12px 0`,borderRadius:12,'
    'background:`#7c3aed`,color:`#fff`,fontWeight:700,fontSize:14,'
    'cursor:`pointer`,textDecoration:`none`,textAlign:`center`},'
    'children:`Open Mod Panel`})'
)
if OLD_ORDER in content:
    content = content.replace(OLD_ORDER, NEW_ORDER, 1)
    print('OK: mod panel btn moved below logout, matched in size')
else:
    errors.append('FAIL: D section button order not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
