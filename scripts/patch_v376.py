#!/usr/bin/env python3
"""Patch v375 -> v376:
- Post page (Wr) invite: add confirm dialog + call P() to refresh post+comments on success
- Postcard (Ir) invite: add confirm dialog
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v375.js'
dst = '_deploy/assets/index-DUcNPOLc-v376.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Post page (Wr) invite: confirm + refresh post & comments ────────────────
WR_OLD = (
    'onClick:()=>{fetch(`${R}/invite-to-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:c.id,invite_username:_u.username,browser_id:Gn()})}).then(()=>{_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);});}'
)
WR_NEW = (
    'onClick:()=>{if(!confirm(`Add ${_u.username} to this huddle?`))return;'
    'fetch(`${R}/invite-to-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:c.id,invite_username:_u.username,browser_id:Gn()})}).then(async _r=>{if(_r.ok){P();_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);}});}'
)
if WR_OLD in content:
    content = content.replace(WR_OLD, WR_NEW, 1)
    print('OK: Wr invite has confirm + P() refresh')
else:
    errors.append('FAIL: Wr invite handler not found')

# ── 2. Postcard (Ir) invite: add confirm dialog ────────────────────────────────
IR_OLD = (
    'onClick:()=>{if(_invSending)return;_setInvSending(!0);'
    'fetch(`${R}/invite-to-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:e.id,invite_username:_u.username,browser_id:Gn()})}).then(()=>{_setInvR([]);_setInvQ(``);_setInvOpen(!1);}).finally(()=>_setInvSending(!1));}'
)
IR_NEW = (
    'onClick:()=>{if(_invSending)return;if(!confirm(`Add ${_u.username} to this huddle?`))return;'
    '_setInvSending(!0);'
    'fetch(`${R}/invite-to-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:e.id,invite_username:_u.username,browser_id:Gn()})}).then(()=>{_setInvR([]);_setInvQ(``);_setInvOpen(!1);}).finally(()=>_setInvSending(!1));}'
)
if IR_OLD in content:
    content = content.replace(IR_OLD, IR_NEW, 1)
    print('OK: Ir invite has confirm dialog')
else:
    errors.append('FAIL: Ir invite handler not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
