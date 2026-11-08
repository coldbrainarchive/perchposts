#!/usr/bin/env python3
"""Patch v437 -> v438:
1. Post page invite: filter already-in-huddle users from search results
2. Post page invite: remove confirm() dialog (blocks on mobile); rely on backend validation
3. New post form: already filtered — no change needed there
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v437.js'
dst = '_deploy/assets/index-DUcNPOLc-v438.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1+2. Post page invite: filter existing members + remove confirm() ─────────
OLD_INV = ('_wpInvR.slice(0,6).map(_u=>(0,L.jsx)(`button`,{type:`button`,'
           'style:{display:`flex`,width:`100%`,padding:`4px 6px`,border:`none`,background:`none`,cursor:`pointer`,borderRadius:6},'
           'onClick:()=>{if(!confirm(`Add ${_u.username} to this huddle?`))return;')
NEW_INV = ('_wpInvR.filter(_u=>{const _em=[c.username,...JSON.parse(c.huddle_members||`[]`).map(_m=>{const _ci=(_m||``).lastIndexOf(`:`);if(_ci>0){const _r=_m.slice(_ci+1);if(_r===`admin`||_r===`mod`)return _m.slice(0,_ci);}return _m||``;})];return!_em.some(_e=>(_e||``).toLowerCase()===(_u.username||``).toLowerCase());}).slice(0,6)'
           '.map(_u=>(0,L.jsx)(`button`,{type:`button`,'
           'style:{display:`flex`,width:`100%`,padding:`4px 6px`,border:`none`,background:`none`,cursor:`pointer`,borderRadius:6},'
           'onClick:()=>{')
if OLD_INV in content:
    content = content.replace(OLD_INV, NEW_INV, 1)
    print('OK: post page invite — existing members filtered + confirm() removed')
else:
    errors.append('FAIL: post page invite button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
