#!/usr/bin/env python3
"""Patch v438 -> v440: Two-tap invite confirmation — inline, no block-body conversion."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v438.js'
dst = '_deploy/assets/index-DUcNPOLc-v440.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add _wpInvP state ──────────────────────────────────────────────────────
OLD_STATE = '[_wpInvOpen,_setWpInvOpen]=(0,_.useState)(!1),[_wpInvQ,_setWpInvQ]=(0,_.useState)(``),[_wpInvR,_setWpInvR]=(0,_.useState)([])'
NEW_STATE = '[_wpInvOpen,_setWpInvOpen]=(0,_.useState)(!1),[_wpInvQ,_setWpInvQ]=(0,_.useState)(``),[_wpInvR,_setWpInvR]=(0,_.useState)([]),[_wpInvP,_setWpInvP]=(0,_.useState)(null)'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: _wpInvP state added')
else:
    errors.append('FAIL: state declarations not found')

# ── 2. Reset _wpInvP on close ─────────────────────────────────────────────────
OLD_CLOSE = '_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);'
NEW_CLOSE = '_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);_setWpInvP(null);'
if OLD_CLOSE in content:
    content = content.replace(OLD_CLOSE, NEW_CLOSE, 1)
    print('OK: _wpInvP reset on close')
else:
    errors.append('FAIL: close handler not found')

# ── 3. Inline two-tap: change style + onClick, keep map as expression arrow ───
OLD_BTN = ('}).slice(0,6).map(_u=>(0,L.jsx)(`button`,{type:`button`,'
           'style:{display:`flex`,width:`100%`,padding:`4px 6px`,border:`none`,background:`none`,cursor:`pointer`,borderRadius:6},'
           'onClick:()=>{')
NEW_BTN = ('}).slice(0,6).map(_u=>(0,L.jsx)(`button`,{type:`button`,'
           'style:{display:`flex`,width:`100%`,padding:`4px 6px`,border:`none`,'
           'background:_wpInvP?.username===_u.username?`rgba(192,132,252,0.15)`:`none`,'
           'outline:_wpInvP?.username===_u.username?`1px solid rgba(192,132,252,0.4)`:`none`,'
           'cursor:`pointer`,borderRadius:6},'
           'onClick:()=>{if(_wpInvP?.username!==_u.username){_setWpInvP(_u);return;}')
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: two-tap inline confirmation added')
else:
    errors.append('FAIL: invite map button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
