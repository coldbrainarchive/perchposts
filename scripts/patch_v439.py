#!/usr/bin/env python3
"""Patch v438 -> v439:
Replace removed confirm() with inline two-tap confirmation:
- First tap: highlights the user (pending state)
- Second tap on the highlighted user: sends invite
Works on both desktop and mobile.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v438.js'
dst = '_deploy/assets/index-DUcNPOLc-v439.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add _wpInvP (pending user) state ───────────────────────────────────────
OLD_STATE = '[_wpInvOpen,_setWpInvOpen]=(0,_.useState)(!1),[_wpInvQ,_setWpInvQ]=(0,_.useState)(``),[_wpInvR,_setWpInvR]=(0,_.useState)([])'
NEW_STATE = '[_wpInvOpen,_setWpInvOpen]=(0,_.useState)(!1),[_wpInvQ,_setWpInvQ]=(0,_.useState)(``),[_wpInvR,_setWpInvR]=(0,_.useState)([]),[_wpInvP,_setWpInvP]=(0,_.useState)(null)'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: _wpInvP state added')
else:
    errors.append('FAIL: _wpInv state declarations not found')

# ── 2. Reset _wpInvP when invite dropdown closes ──────────────────────────────
OLD_CLOSE = '_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);'
NEW_CLOSE = '_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);_setWpInvP(null);'
if OLD_CLOSE in content:
    content = content.replace(OLD_CLOSE, NEW_CLOSE, 1)
    print('OK: _wpInvP reset on close')
else:
    errors.append('FAIL: invite close handler not found')

# ── 3. Replace invite button with two-tap inline confirmation ─────────────────
OLD_BTN = ('_wpInvR.filter(_u=>{const _em=[c.username,...JSON.parse(c.huddle_members||`[]`).map(_m=>{const _ci=(_m||``).lastIndexOf(`:`);if(_ci>0){const _r=_m.slice(_ci+1);if(_r===`admin`||_r===`mod`)return _m.slice(0,_ci);}return _m||``;})];return!_em.some(_e=>(_e||``).toLowerCase()===(_u.username||``).toLowerCase());}).slice(0,6)'
           '.map(_u=>(0,L.jsx)(`button`,{type:`button`,'
           'style:{display:`flex`,width:`100%`,padding:`4px 6px`,border:`none`,background:`none`,cursor:`pointer`,borderRadius:6},'
           'onClick:()=>{')
NEW_BTN = ('_wpInvR.filter(_u=>{const _em=[c.username,...JSON.parse(c.huddle_members||`[]`).map(_m=>{const _ci=(_m||``).lastIndexOf(`:`);if(_ci>0){const _r=_m.slice(_ci+1);if(_r===`admin`||_r===`mod`)return _m.slice(0,_ci);}return _m||``;})];return!_em.some(_e=>(_e||``).toLowerCase()===(_u.username||``).toLowerCase());}).slice(0,6)'
           '.map(_u=>{const _isPending=_wpInvP?.username===_u.username;return(0,L.jsx)(`button`,{type:`button`,'
           'style:{display:`flex`,width:`100%`,padding:`4px 6px`,border:`none`,background:_isPending?`rgba(192,132,252,0.15)`:`none`,borderRadius:6,cursor:`pointer`,outline:_isPending?`1px solid rgba(192,132,252,0.4)`:`none`},'
           'onClick:()=>{if(!_isPending){_setWpInvP(_u);return;}')
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: invite button uses two-tap inline confirmation')
else:
    errors.append('FAIL: invite button not found')

# ── 4. Close the new arrow-function and map correctly (add }) ─────────────────
# The map now uses an arrow with block body — need to close the block after children
# Find the old closing pattern: ...,children:(jsx)},_u.username))
# and add the closing } for the block body
OLD_MAP_CLOSE = '},_u.username))})]})]})'
NEW_MAP_CLOSE = '};},_u.username))})]})]})'
if OLD_MAP_CLOSE in content:
    content = content.replace(OLD_MAP_CLOSE, NEW_MAP_CLOSE, 1)
    print('OK: map block body closed correctly')
else:
    errors.append('FAIL: map close pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
