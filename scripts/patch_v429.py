#!/usr/bin/env python3
"""Patch v428 -> v429:
1. Add global _adminUsers Set — auto-populated whenever admin is detected,
   so Jn always gives the correct top-hat bird from username alone.
2. Search chip admin check: case-insensitive + populates _adminUsers.
3. Invite: carry :admin/:mod suffix so new invitees show correct pill.
4. Postcard gap: tighten top padding to 4px when no title.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v428.js'
dst = '_deploy/assets/index-DUcNPOLc-v429.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Declare _adminUsers Set alongside _jailed/_banned ─────────────────────
OLD_SETS = 'var _jailed=new Set(),_banned=new Set();'
NEW_SETS = 'var _jailed=new Set(),_banned=new Set(),_adminUsers=new Set();'
if OLD_SETS in content:
    content = content.replace(OLD_SETS, NEW_SETS, 1)
    print('OK: _adminUsers Set declared')
else:
    errors.append('FAIL: Set declarations not found')

# ── 2. Jn: check _adminUsers before hash; populate when is_admin ──────────────
OLD_JN = 'if(e.is_admin)return{e:null,f:``,s:null,hat:!0};'
NEW_JN = ('if(e.username&&_adminUsers.has(e.username.toLowerCase()))return{e:null,f:``,s:null,hat:!0};'
          'if(e.is_admin){if(e.username)_adminUsers.add(e.username.toLowerCase());return{e:null,f:``,s:null,hat:!0};}')
if OLD_JN in content:
    content = content.replace(OLD_JN, NEW_JN, 1)
    print('OK: Jn checks+populates _adminUsers')
else:
    errors.append('FAIL: Jn is_admin line not found')

# ── 3. Search chip admin check: case-insensitive + populate _adminUsers ───────
OLD_CHIP_ADMIN = '(UR.find(_f=>_f.username===m)||{}).role===`admin`?`#ffffff`:Hn(null,m)'
NEW_CHIP_ADMIN = ('(()=>{const _ua=UR.find(_f=>_f.username.toLowerCase()===m.toLowerCase());'
                  'if(_ua?.role===`admin`)_adminUsers.add(m.toLowerCase());'
                  'return _ua?.role===`admin`;})()?`#ffffff`:Hn(null,m)')
if OLD_CHIP_ADMIN in content:
    content = content.replace(OLD_CHIP_ADMIN, NEW_CHIP_ADMIN, 1)
    print('OK: chip background admin check case-insensitive + populates _adminUsers')
else:
    errors.append('FAIL: chip background admin check not found')

OLD_CHIP_IMG = '(UR.find(_f=>_f.username===m)||{}).role===`admin`?(0,L.jsx)(`img`,{src:`/admin-bird.png`'
NEW_CHIP_IMG = '_adminUsers.has(m.toLowerCase())?(0,L.jsx)(`img`,{src:`/admin-bird.png`'
if OLD_CHIP_IMG in content:
    content = content.replace(OLD_CHIP_IMG, NEW_CHIP_IMG, 1)
    print('OK: chip bird uses _adminUsers for admin detection')
else:
    errors.append('FAIL: chip bird admin check not found')

# ── 4. Search results handler: populate _adminUsers when admin found ──────────
OLD_SETUR = 'if(_d.users&&_d.users.length)setUR(_d.users);'
NEW_SETUR = ('if(_d.users&&_d.users.length){'
             '_d.users.forEach(_u=>{if(_u.role===`admin`&&_u.username)_adminUsers.add(_u.username.toLowerCase());});'
             'setUR(_d.users);}')
if OLD_SETUR in content:
    content = content.replace(OLD_SETUR, NEW_SETUR, 1)
    print('OK: search results populate _adminUsers')
else:
    errors.append('FAIL: setUR handler not found')

# ── 5. Invite: send role suffix for admin/mod ─────────────────────────────────
OLD_INV = 'invite_username:_u.username,browser_id:Gn()'
NEW_INV = 'invite_username:(_u.role===`admin`||_u.role===`mod`)?`${_u.username}:${_u.role}`:_u.username,browser_id:Gn()'
if OLD_INV in content:
    content = content.replace(OLD_INV, NEW_INV, 1)
    print('OK: invite sends role suffix for admin/mod')
else:
    errors.append('FAIL: invite_username not found')

# ── 6. Postcard gap: tighten padding when no title ────────────────────────────
OLD_PAD = 'padding:t?`16px 14px`:`10px 14px`'
NEW_PAD = 'padding:t?`16px 14px`:`4px 14px`'
if OLD_PAD in content:
    content = content.replace(OLD_PAD, NEW_PAD, 1)
    print('OK: no-title postcard paddingTop 10->4px')
else:
    errors.append('FAIL: postcard padding not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
