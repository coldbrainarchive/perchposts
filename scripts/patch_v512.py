#!/usr/bin/env python3
"""Patch v511 -> v512: Fix is_mod missing from Xn records so mod pills show purple everywhere."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v511.js'
dst = '_deploy/assets/index-DUcNPOLc-v512.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add _modUsers Set + _addMod function next to _adminUsers ───────────────
OLD_ADMIN_SET = ('var _adminUsers=(()=>{try{return new Set(JSON.parse(localStorage.getItem(`_au`)||`[]`));}catch(_){return new Set();}})();'
                 'function _addAdmin(u){if(!u)return;const l=u.toLowerCase();if(_adminUsers.has(l))return;_adminUsers.add(l);try{const c=JSON.parse(localStorage.getItem(`_au`)||`[]`);c.push(l);localStorage.setItem(`_au`,JSON.stringify(c));}catch(_){}}')
NEW_ADMIN_SET  = ('var _adminUsers=(()=>{try{return new Set(JSON.parse(localStorage.getItem(`_au`)||`[]`));}catch(_){return new Set();}})();'
                  'function _addAdmin(u){if(!u)return;const l=u.toLowerCase();if(_adminUsers.has(l))return;_adminUsers.add(l);try{const c=JSON.parse(localStorage.getItem(`_au`)||`[]`);c.push(l);localStorage.setItem(`_au`,JSON.stringify(c));}catch(_){}}'
                  'var _modUsers=(()=>{try{return new Set(JSON.parse(localStorage.getItem(`_mu`)||`[]`));}catch(_){return new Set();}})();'
                  'function _addMod(u){if(!u)return;const l=u.toLowerCase();if(_modUsers.has(l))return;_modUsers.add(l);try{const c=JSON.parse(localStorage.getItem(`_mu`)||`[]`);c.push(l);localStorage.setItem(`_mu`,JSON.stringify(c));}catch(_){}}')
if OLD_ADMIN_SET in content:
    content = content.replace(OLD_ADMIN_SET, NEW_ADMIN_SET, 1)
    print('OK: _modUsers set + _addMod added')
else:
    errors.append('FAIL: _adminUsers block not found')

# ── 2. Call _addMod in Jn() when e.is_mod is true ────────────────────────────
OLD_JN_ADMIN = 'if(e.is_admin){if(e.username)_addAdmin(e.username);return{e:null,f:``,s:null,hat:!0};}'
NEW_JN_ADMIN = 'if(e.is_admin){if(e.username)_addAdmin(e.username);return{e:null,f:``,s:null,hat:!0};}if(e.is_mod&&e.username)_addMod(e.username);'
if OLD_JN_ADMIN in content:
    content = content.replace(OLD_JN_ADMIN, NEW_JN_ADMIN, 1)
    print('OK: _addMod call added in Jn()')
else:
    errors.append('FAIL: Jn is_admin block not found')

# ── 3. Search filter chip: add is_mod ────────────────────────────────────────
OLD_SEARCH_CHIP = 'record:{username:m,browser_id:null,is_admin:_adminUsers.has(m.toLowerCase())},name:m,color:Hn(null,m)'
NEW_SEARCH_CHIP = 'record:{username:m,browser_id:null,is_admin:_adminUsers.has(m.toLowerCase()),is_mod:_modUsers.has(m.toLowerCase())&&!_adminUsers.has(m.toLowerCase())},name:m,color:Hn(null,m)'
if OLD_SEARCH_CHIP in content:
    content = content.replace(OLD_SEARCH_CHIP, NEW_SEARCH_CHIP, 1)
    print('OK: search chip is_mod added')
else:
    errors.append('FAIL: search chip record not found')

# ── 4. Pre-huddle member list (create post): add is_mod from role ─────────────
OLD_PREHUDDLE = ('record:{username:_u.username,browser_id:_u.browser_id,is_admin:_u.role===`admin`},'
                 'name:_u.username,color:Hn(_u.browser_id,_u.username)},_u.username))})]}):s&&')
NEW_PREHUDDLE = ('record:{username:_u.username,browser_id:_u.browser_id,is_admin:_u.role===`admin`,is_mod:_u.role===`mod`},'
                 'name:_u.username,color:Hn(_u.browser_id,_u.username)},_u.username))})]}):s&&')
if OLD_PREHUDDLE in content:
    content = content.replace(OLD_PREHUDDLE, NEW_PREHUDDLE, 1)
    print('OK: pre-huddle member list is_mod added')
else:
    errors.append('FAIL: pre-huddle member list not found')

# ── 5. Post page huddle member list: add is_mod from role ────────────────────
OLD_POSTHUDDLE = ('record:{username:_u.username,browser_id:_u.browser_id,is_admin:_u.role===`admin`},'
                  'name:_u.username,color:Hn(_u.browser_id,_u.username),onClick:_u.username?()=>o(`/?user=${encodeURIC')
NEW_POSTHUDDLE = ('record:{username:_u.username,browser_id:_u.browser_id,is_admin:_u.role===`admin`,is_mod:_u.role===`mod`},'
                  'name:_u.username,color:Hn(_u.browser_id,_u.username),onClick:_u.username?()=>o(`/?user=${encodeURIC')
if OLD_POSTHUDDLE in content:
    content = content.replace(OLD_POSTHUDDLE, NEW_POSTHUDDLE, 1)
    print('OK: post page huddle member list is_mod added')
else:
    errors.append('FAIL: post page huddle member list not found')

# ── 6. Remove picker: add is_mod from role ────────────────────────────────────
OLD_REM = 'record:{username:_m.u,browser_id:null,is_admin:_m.r===`admin`},name:_m.u,color:Hn(null,_m.u)'
NEW_REM = 'record:{username:_m.u,browser_id:null,is_admin:_m.r===`admin`,is_mod:_m.r===`mod`},name:_m.u,color:Hn(null,_m.u)'
if OLD_REM in content:
    content = content.replace(OLD_REM, NEW_REM, 1)
    print('OK: remove picker is_mod added')
else:
    errors.append('FAIL: remove picker record not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
