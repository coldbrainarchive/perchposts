#!/usr/bin/env python3
"""Patch v513 -> v514: Fix mod purple in search dropdown and invite picker."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v513.js'
dst = '_deploy/assets/index-DUcNPOLc-v514.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Call _addMod when search-users results load (main search) ──────────────
OLD_ADD_ADMIN = ('_d.users.forEach(_u=>{if(_u.role===`admin`&&_u.username)_addAdmin(_u.username);});setUR(_d.users);}')
NEW_ADD_ADMIN = ('_d.users.forEach(_u=>{if(_u.role===`admin`&&_u.username)_addAdmin(_u.username);if(_u.role===`mod`&&_u.username)_addMod(_u.username);});setUR(_d.users);}')
if OLD_ADD_ADMIN in content:
    content = content.replace(OLD_ADD_ADMIN, NEW_ADD_ADMIN, 1)
    print('OK: _addMod called in search-users load')
else:
    errors.append('FAIL: search-users _addAdmin forEach not found')

# ── 2. Fix background in main search dropdown pill ────────────────────────────
OLD_UR_BG = ('background:_u.role===`admin`?`#ffffff`:Hn(null,_u.username),color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1,flexShrink:0,boxSizing:`border-box`}')
NEW_UR_BG = ('background:_u.role===`admin`?`#ffffff`:_u.role===`mod`?`#c084fc`:Hn(null,_u.username),color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1,flexShrink:0,boxSizing:`border-box`}')
if OLD_UR_BG in content:
    content = content.replace(OLD_UR_BG, NEW_UR_BG, 1)
    print('OK: search dropdown pill background fixed for mods')
else:
    errors.append('FAIL: search dropdown pill background not found')

# ── 3. Fix Jn call in search dropdown to pass is_mod ─────────────────────────
OLD_UR_JN = 'Jn({username:_u.username,browser_id:null,is_admin:_u.role===`admin`})||{}'
NEW_UR_JN = 'Jn({username:_u.username,browser_id:null,is_admin:_u.role===`admin`,is_mod:_u.role===`mod`})||{}'
if OLD_UR_JN in content:
    content = content.replace(OLD_UR_JN, NEW_UR_JN)
    print('OK: search dropdown Jn is_mod added')
else:
    errors.append('FAIL: search dropdown Jn call not found')

# ── 4. Fix background in invite picker pill ───────────────────────────────────
OLD_INV_BG = ('background:_u.role===`admin`?`#ffffff`:Hn(_u.browser_id||null,_u.username),color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1}')
NEW_INV_BG = ('background:_u.role===`admin`?`#ffffff`:_u.role===`mod`?`#c084fc`:Hn(_u.browser_id||null,_u.username),color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1}')
if OLD_INV_BG in content:
    content = content.replace(OLD_INV_BG, NEW_INV_BG, 1)
    print('OK: invite picker pill background fixed for mods')
else:
    errors.append('FAIL: invite picker pill background not found')

# ── 5. Fix Jn call in invite picker to pass is_mod ───────────────────────────
OLD_INV_JN = 'Jn({username:_u.username,browser_id:_u.browser_id||null,is_admin:_u.role===`admin`})||{}'
NEW_INV_JN = 'Jn({username:_u.username,browser_id:_u.browser_id||null,is_admin:_u.role===`admin`,is_mod:_u.role===`mod`})||{}'
if OLD_INV_JN in content:
    content = content.replace(OLD_INV_JN, NEW_INV_JN, 1)
    print('OK: invite picker Jn is_mod added')
else:
    errors.append('FAIL: invite picker Jn call not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
