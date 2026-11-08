#!/usr/bin/env python3
"""Patch v834 -> v835: an account Trash for the admin. Deleted accounts wait in the Mod Panel, greyed out,
with Bring back and Delete forever. Delete messages stop saying it can't be undone, because now it can.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v834.js'
dst = '_deploy/assets/index-DUcNPOLc-v835.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): expected ' + str(count) + ' matches, found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

patch(t('`This can\'t be undone. Your posts and chirps stay on the site, shown as Extinct Bird, and your username is retired forever. Delete anything you want gone first.`'),
      t('`Your posts and chirps stay on the site, shown as Extinct Bird, and you won\'t be able to sign in. An admin can bring your account back if you ask. Delete anything you want gone first.`'), 'self delete wording')
patch(t('children:_dlB?`…`:`Delete forever`'), t('children:_dlB?`…`:`Delete account`'), 'self delete button')
patch(t('`Delete ${i||`this flock member`}? This cannot be undone.`'),
      t('`Delete ${i||`this flock member`}? They\'ll go to the Trash, where an admin can bring them back.`'), 'mod delete wording')

patch(t('[_expId,_setExpId]=(0,_.useState)(null),_e=(0,_.useCallback)(async()=>{let e=$n(),[t,r,a,s]=await Promise.all([fetch(`${R}/get-mod-data`,{headers:e}),fetch(`${R}/get-members`,{headers:e}),fetch(`${R}/bot-config`,{headers:e}),fetch(`${R}/bot-logs`,{headers:e})]),l='),
      t('[_expId,_setExpId]=(0,_.useState)(null),[_tr,_setTr]=(0,_.useState)([]),_e=(0,_.useCallback)(async()=>{let e=$n(),[t,r,a,s,_tq]=await Promise.all([fetch(`${R}/get-mod-data`,{headers:e}),fetch(`${R}/get-members`,{headers:e}),fetch(`${R}/bot-config`,{headers:e}),fetch(`${R}/bot-logs`,{headers:e}),fetch(`${R}/get-trash`,{headers:e})]);_setTr(_tq.ok?(await _tq.json()).accounts||[]:[]);let l='),
      'load trash')
patch(t('children:`Delete`})]})]},n.id)})]})]})})(),(0,L.jsxs)(`div`,{className:`content-card`,style:{padding:0,overflow:`hidd'),
      t('children:`Delete`})]})]},n.id)})]})]})})(),_tr.length>0&&(0,L.jsxs)(`div`,{className:`content-card account-trash`,style:{padding:0,overflow:`hidden`},children:[(0,L.jsx)(`div`,{style:{padding:`12px 14px`,fontSize:13,fontWeight:700,color:`#94a3b8`,borderBottom:`1px solid #2e303a`},children:`🗑️ Trash (${_tr.length})`}),..._tr.map(_a=>(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8,padding:`10px 14px`,borderBottom:`1px solid #2e303a`},children:[(0,L.jsxs)(`div`,{style:{flex:1,minWidth:0,opacity:.6},children:[(0,L.jsx)(`div`,{style:{fontSize:13,fontWeight:700,color:`#cbd5e1`,overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`},children:_a.username}),(0,L.jsx)(`div`,{style:{fontSize:11,color:`#64748b`,marginTop:2},children:(_a.deleted_by===`self`?`Deleted their account`:`Deleted by a mod`)+` · `+Un(_a.deleted_at)})]}),(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Bring ${_a.username} back?`))return;let _r=await fetch(`${R}/restore-member`,{method:`POST`,headers:{"Content-Type":`application/json`,...$n()},body:JSON.stringify({user_id:_a.id})});if(!_r.ok)alert(`Could not bring them back`);_e()},style:{padding:`4px 10px`,borderRadius:6,border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:11,cursor:`pointer`,whiteSpace:`nowrap`},children:`Bring back`}),(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Delete ${_a.username} forever? They can never come back. Their posts stay as Extinct Bird and the name stays retired.`))return;let _r=await fetch(`${R}/purge-member`,{method:`POST`,headers:{"Content-Type":`application/json`,...$n()},body:JSON.stringify({user_id:_a.id})});if(!_r.ok)alert(`Could not delete them`);_e()},style:{padding:`4px 10px`,borderRadius:6,border:`1px solid #374151`,background:`transparent`,color:`#f87171`,fontWeight:600,fontSize:11,cursor:`pointer`,whiteSpace:`nowrap`},children:`Delete forever`})]},_a.id))]}),(0,L.jsxs)(`div`,{className:`content-card`,style:{padding:0,overflow:`hidd'),
      'trash list')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
