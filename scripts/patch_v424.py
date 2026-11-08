#!/usr/bin/env python3
"""Patch v423 -> v424:
Store browser_id + role with each huddle member so pills show the correct
bird emoji and background colour everywhere. Backward compatible with old
huddles that stored plain username strings.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v423.js'
dst = '_deploy/assets/index-DUcNPOLc-v424.js'

content = open(src, encoding='utf-8').read()
errors = []

# shared normaliser inline — converts old string OR new {u,b,r} object
_NORM = (
    'const _normHm=_x=>typeof _x===`string`'
    '?{username:_x,browser_id:null,role:null}'
    ':{username:_x.u||_x,browser_id:_x.b||null,role:_x.r||null};'
)

# ── 1. create-post: store full objects instead of plain usernames ─────────────
OLD_CREATE = 'huddle_members:_isHuddle?_hmTagged.map(_u=>_u.username):[]'
NEW_CREATE  = 'huddle_members:_isHuddle?_hmTagged.map(_u=>({u:_u.username,b:_u.browser_id||null,r:_u.role||null})):[]'
if OLD_CREATE in content:
    content = content.replace(OLD_CREATE, NEW_CREATE, 1)
    print('OK: create-post stores {u,b,r} per member')
else:
    errors.append('FAIL: create-post huddle_members not found')

# ── 2. feed: normalise parsed members; _fHm is now [{username,browser_id,role}]
OLD_FEED_HM = 'const _hm=JSON.parse(e.huddle_members||`[]`);_fHm=_hm.filter(Boolean);return`Huddle with: ${_fHm.join(`, `)}`'
NEW_FEED_HM = (
    'const _hm=JSON.parse(e.huddle_members||`[]`);'
    + _NORM
    + '_fHm=_hm.filter(Boolean).map(_normHm);'
    + 'return`Huddle with: ${_fHm.map(_x=>_x.username).join(`, `)}`'
)
if OLD_FEED_HM in content:
    content = content.replace(OLD_FEED_HM, NEW_FEED_HM, 1)
    print('OK: feed normalises member objects')
else:
    errors.append('FAIL: feed hm computation not found')

# ── 3. Pr postcard pills: use normalised {username,browser_id,role} ───────────
OLD_PR_PILLS = '_prHm.map(_u=>(0,L.jsx)(Xn,{record:{username:_u,browser_id:null},name:_u,color:Hn(null,_u)},_u))'
NEW_PR_PILLS = '_prHm.map(_u=>(0,L.jsx)(Xn,{record:{username:_u.username,browser_id:_u.browser_id,is_admin:_u.role===`admin`},name:_u.username,color:Hn(_u.browser_id,_u.username)},_u.username))'
if OLD_PR_PILLS in content:
    content = content.replace(OLD_PR_PILLS, NEW_PR_PILLS, 1)
    print('OK: Pr pills use full member data')
else:
    errors.append('FAIL: Pr pills not found')

# ── 4. post page: normalise parsed members ────────────────────────────────────
OLD_PP_HM = 'const _hm=JSON.parse(c.huddle_members||`[]`).filter(Boolean);return _hm'
NEW_PP_HM  = (
    'const _hm=JSON.parse(c.huddle_members||`[]`).filter(Boolean);'
    + _NORM
    + 'return _hm.map(_normHm)'
)
if OLD_PP_HM in content:
    content = content.replace(OLD_PP_HM, NEW_PP_HM, 1)
    print('OK: post page normalises member objects')
else:
    errors.append('FAIL: post page hm computation not found')

# ── 5. post page pills: use normalised {username,browser_id,role} ─────────────
OLD_PP_PILLS = 'e.map(_u=>(0,L.jsx)(Xn,{record:{username:_u,browser_id:null},name:_u,color:Hn(null,_u)},_u))'
NEW_PP_PILLS = 'e.map(_u=>(0,L.jsx)(Xn,{record:{username:_u.username,browser_id:_u.browser_id,is_admin:_u.role===`admin`},name:_u.username,color:Hn(_u.browser_id,_u.username)},_u.username))'
if OLD_PP_PILLS in content:
    content = content.replace(OLD_PP_PILLS, NEW_PP_PILLS, 1)
    print('OK: post page pills use full member data')
else:
    errors.append('FAIL: post page pills not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
