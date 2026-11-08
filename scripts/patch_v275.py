#!/usr/bin/env python3
"""Patch v274 -> v275: DM inbox shows a register/login prompt for unauthenticated
users instead of the misleading 'No messages yet' empty state. Also the dm-inbox
fetch is skipped entirely when there's no auth token to avoid the silent 401."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v274.js'
dst = '_deploy/assets/index-DUcNPOLc-v275.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Replace inbox empty state with auth-aware state ────────────────────────
# Current: always shows "No messages yet" + hint text (even when user isn't logged in)
# New: if no auth_token, show "Register or log in to use direct messages"
#      if logged in but no convs, show the existing hint
OLD_EMPTY = (
    '(0,L.jsxs)(`div`,{style:{padding:`48px 20px`,color:`#64748b`,textAlign:`center`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`No messages yet`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:12,marginTop:4},'
    'children:`Search for a user and tap Message to start a chat`})]})'
)
NEW_EMPTY = (
    'localStorage.getItem(`auth_token`)?'
    '(0,L.jsxs)(`div`,{style:{padding:`48px 20px`,color:`#64748b`,textAlign:`center`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`No messages yet`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:12,marginTop:4},'
    'children:`Search for a user and tap Message to start a chat`})]}):'
    '(0,L.jsxs)(`div`,{style:{padding:`48px 20px`,color:`#64748b`,textAlign:`center`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:32,marginBottom:8},children:`🔒`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600,color:`#f1f5f9`},children:`Register to use direct messages`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:12,marginTop:6,lineHeight:1.5},'
    'children:`Create a free account to send and receive private messages with other users.`})]})'
)
if OLD_EMPTY in content:
    content = content.replace(OLD_EMPTY, NEW_EMPTY, 1)
    print('OK: inbox shows register prompt for unauthenticated users')
else:
    errors.append('FAIL: inbox empty state not found')

# ── 2. Skip dm-inbox fetch when no auth token ─────────────────────────────────
# Current: always fetches (gets silent 401 for unauthenticated users)
# New: only fetch if localStorage has auth_token
OLD_FETCH = (
    'c===`inbox`&&!_dmThread&&(async()=>{let _r=await fetch(`${R}/dm-inbox`,{headers:er()});'
    '_setDmConvs((_r.ok?await _r.json():{}).conversations||[])})()'
)
NEW_FETCH = (
    'c===`inbox`&&!_dmThread&&localStorage.getItem(`auth_token`)&&'
    '(async()=>{let _r=await fetch(`${R}/dm-inbox`,{headers:er()});'
    'if(_r.status===401){localStorage.removeItem(`auth_token`);localStorage.removeItem(`auth_user`);_setDmConvs([]);return;}'
    '_setDmConvs((_r.ok?await _r.json():{}).conversations||[])})()'
)
if OLD_FETCH in content:
    content = content.replace(OLD_FETCH, NEW_FETCH, 1)
    print('OK: dm-inbox fetch skips when no auth token; clears stale token on 401')
else:
    errors.append('FAIL: dm-inbox fetch not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
