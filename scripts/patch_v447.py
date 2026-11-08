#!/usr/bin/env python3
"""Patch v446 -> v447:
Inline invite button:
- Add req_username to body so mobile (different browser_id) can be verified as creator
- Add error handling so failures are surfaced instead of silent
- Add touchAction:manipulation to prevent iOS click delay
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v446.js'
dst = '_deploy/assets/index-DUcNPOLc-v447.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Fix the invite fetch: add req_username, error handling, catch ──────────
OLD_FETCH = ('fetch(`${R}/invite-to-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
             'body:JSON.stringify({post_id:c.id,'
             'invite_username:(_wpInvP.role===`admin`||_wpInvP.role===`mod`)?`${_wpInvP.username}:${_wpInvP.role}`:_wpInvP.username,'
             'browser_id:Gn()})}).then(async _r=>{if(_r.ok){const _ij=await _r.json().catch(()=>({}));if(_ij.post)l(Cr(_ij.post));'
             'const _sc=_ij.systemComment||{id:`__sys_${Date.now()}`,content:`👥 ${_wpInvP.username} was added to the huddle`,'
             'username:`__system__`,created_at:new Date().toISOString(),browser_id:null,parent_comment_id:null,is_mod:0};'
             'd(e=>[...e,_sc]);_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);_setWpInvP(null);}});')
NEW_FETCH = ('fetch(`${R}/invite-to-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
             'body:JSON.stringify({post_id:c.id,'
             'invite_username:(_wpInvP.role===`admin`||_wpInvP.role===`mod`)?`${_wpInvP.username}:${_wpInvP.role}`:_wpInvP.username,'
             'browser_id:Gn(),req_username:localStorage.getItem(`_myUsername`)||null})}).then(async _r=>{'
             'const _ij=await _r.json().catch(()=>({}));'
             'if(!_r.ok){alert(_ij.error||`Could not invite user`);return;}'
             'if(_ij.post)l(Cr(_ij.post));'
             'const _sc=_ij.systemComment||{id:`__sys_${Date.now()}`,content:`👥 ${_wpInvP.username} was added to the huddle`,'
             'username:`__system__`,created_at:new Date().toISOString(),browser_id:null,parent_comment_id:null,is_mod:0};'
             'd(e=>[...e,_sc]);_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);_setWpInvP(null);'
             '}).catch(err=>alert(`Invite failed: `+err.message));')
if OLD_FETCH in content:
    content = content.replace(OLD_FETCH, NEW_FETCH, 1)
    print('OK: invite fetch has req_username + error handling + catch')
else:
    errors.append('FAIL: invite fetch not found')

# ── 2. Add touchAction:manipulation to invite button ─────────────────────────
OLD_BTN_STYLE = 'style:{width:`100%`,marginTop:6,padding:`6px 10px`,borderRadius:8,border:`none`,background:`#c084fc`,color:`#fff`,fontWeight:700,fontSize:12,cursor:`pointer`}'
NEW_BTN_STYLE = 'style:{width:`100%`,marginTop:6,padding:`6px 10px`,borderRadius:8,border:`none`,background:`#c084fc`,color:`#fff`,fontWeight:700,fontSize:12,cursor:`pointer`,touchAction:`manipulation`}'
if OLD_BTN_STYLE in content:
    content = content.replace(OLD_BTN_STYLE, NEW_BTN_STYLE, 1)
    print('OK: touchAction:manipulation added to invite button')
else:
    errors.append('FAIL: invite button style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
