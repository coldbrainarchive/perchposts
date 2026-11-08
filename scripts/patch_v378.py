#!/usr/bin/env python3
"""Patch v377 -> v378:
- Wr invite: use d() (u state) instead of v() (g state) with server-returned comment ID
  so the system message isn't wiped by P()'s v([]) call every 2s
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v377.js'
dst = '_deploy/assets/index-DUcNPOLc-v378.js'

content = open(src, encoding='utf-8').read()
errors = []

# v() adds to g (optimistic), which P() clears every 2s via v([])
# d() adds to u (server comments), which P() replaces via d(s) — but s includes
# the system comment if the server has it, so no flicker
OLD = (
    'const _ij=await _r.json().catch(()=>({}));'
    'if(_ij.post)l(Cr(_ij.post));'
    'v(e=>[...e,{id:`__sys_${Date.now()}`,content:`\U0001f465 ${_u.username} was added to the huddle`,'
    'username:`__system__`,created_at:new Date().toISOString(),browser_id:null,parent_comment_id:null,is_mod:!1,isPending:!1}]);'
    '_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);'
)
NEW = (
    'const _ij=await _r.json().catch(()=>({}));'
    'if(_ij.post)l(Cr(_ij.post));'
    # Use server-returned comment (with real ID) so P() poll recognises it and doesn't drop it
    'const _sc=_ij.systemComment||{id:`__sys_${Date.now()}`,content:`\U0001f465 ${_u.username} was added to the huddle`,username:`__system__`,created_at:new Date().toISOString(),browser_id:null,parent_comment_id:null,is_mod:0};'
    'd(e=>[...e,_sc]);'  # d = setter for u (server comment list), not g (wiped by P())
    '_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: invite system comment uses d() with server ID')
else:
    errors.append('FAIL: invite system comment block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
