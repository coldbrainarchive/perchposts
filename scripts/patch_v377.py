#!/usr/bin/env python3
"""Patch v376 -> v377:
- Post page (Wr) invite: read response, update post body immediately, add system comment to g state optimistically
- Also update backend to return systemComment in invite response for reliability
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v376.js'
dst = '_deploy/assets/index-DUcNPOLc-v377.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── Post page (Wr) invite: update post + add system comment immediately ────────
WR_OLD = (
    'onClick:()=>{if(!confirm(`Add ${_u.username} to this huddle?`))return;'
    'fetch(`${R}/invite-to-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:c.id,invite_username:_u.username,browser_id:Gn()})}).then(async _r=>{if(_r.ok){P();_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);}});}'
)
WR_NEW = (
    'onClick:()=>{if(!confirm(`Add ${_u.username} to this huddle?`))return;'
    'fetch(`${R}/invite-to-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:c.id,invite_username:_u.username,browser_id:Gn()})}).then(async _r=>{if(_r.ok){'
    'const _ij=await _r.json().catch(()=>({}));'
    'if(_ij.post)l(Cr(_ij.post));'
    'v(e=>[...e,{id:`__sys_${Date.now()}`,content:`\U0001f465 ${_u.username} was added to the huddle`,'
    'username:`__system__`,created_at:new Date().toISOString(),browser_id:null,parent_comment_id:null,is_mod:!1,isPending:!1}]);'
    '_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);}});}'
)
if WR_OLD in content:
    content = content.replace(WR_OLD, WR_NEW, 1)
    print('OK: Wr invite updates post body + adds system comment immediately')
else:
    errors.append('FAIL: Wr invite handler not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
