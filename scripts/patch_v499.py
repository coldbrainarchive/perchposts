#!/usr/bin/env python3
"""Patch v498 -> v499:
- Remove duplicate pill display above the member list
- Move Remove button below the member list (red, full-width)
- Keep member list pills with red outline on selected
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v498.js'
dst = '_deploy/assets/index-DUcNPOLc-v499.js'

content = open(src, encoding='utf-8').read()

# The fetch/onClick handler for the remove button (reused)
FETCH_HANDLER = (
    'const _rUn2=localStorage.getItem(`_myUsername`)||null;'
    'fetch(`${R}/remove-from-huddle`,{method:`POST`,'
    'headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:c.id,remove_username:_wpRemP.u,'
    'req_username:_rUn2,browser_id:Gn()})}).then(async _rr=>{'
    'const _rj=await _rr.json().catch(()=>({}));'
    'if(!_rr.ok){alert(_rj.error||`Could not remove`);return;}'
    'if(_rj.post)l(Cr(_rj.post));'
    'const _rsc=_rj.systemComment||{id:`__sys_${Date.now()}`,'
    'content:`💨 ${_wpRemP.u} was removed from the huddle`,'
    'username:`__system__`,created_at:new Date().toISOString(),'
    'browser_id:null,parent_comment_id:null,is_mod:0};'
    'd(e=>[...e,_rsc]);_setWpRemOpen(!1);_setWpRemP(null);'
    '}).catch(err=>alert(`Remove failed: `+err.message));'
)

# OLD: duplicate pill section + member list + closing
OLD = (
    '_wpRemP&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,'
    'gap:8,marginBottom:8},children:[(0,L.jsx)(Xn,{record:{username:_wpRemP.u,'
    'browser_id:null,is_admin:_wpRemP.r===`admin`},name:_wpRemP.u,color:Hn(null,_wpRemP.u)}),'
    '(0,L.jsx)(`button`,{type:`button`,style:{width:`100%`,padding:`10px`,borderRadius:10,'
    'border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,'
    'cursor:`pointer`,touchAction:`manipulation`},'
    'onClick:()=>{' + FETCH_HANDLER + '},'
    'children:`Remove `+_wpRemP.u})]}),\n'
    '(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:6},'
    'children:(()=>{const _rUn2=localStorage.getItem(`_myUsername`)||null;'
)

# NEW: just member list + button below
NEW = (
    '(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:6},'
    'children:(()=>{const _rUn2=localStorage.getItem(`_myUsername`)||null;'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: duplicate pill section removed')
else:
    print('FAIL: could not find OLD section'); sys.exit(1)

# Now add the Remove button AFTER the member list, before the closing ]}),
MEMBER_LIST_END = '_m.u)})},_m.u));})()})]}),'
BUTTON_AFTER = (
    '_m.u)})},_m.u));})()})'  # close member list children
    ',_wpRemP&&(0,L.jsx)(`button`,{type:`button`,'
    'style:{width:`100%`,padding:`10px`,borderRadius:10,border:`none`,'
    'background:`#ef4444`,color:`#fff`,fontWeight:700,fontSize:14,'
    'cursor:`pointer`,touchAction:`manipulation`,marginTop:8},'
    'onClick:()=>{' + FETCH_HANDLER + '},'
    'children:`Remove `+_wpRemP.u})'
    ']}),'
)

if MEMBER_LIST_END in content:
    content = content.replace(MEMBER_LIST_END, BUTTON_AFTER, 1)
    print('OK: Remove button added below member list')
else:
    print('FAIL: member list end not found'); sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
