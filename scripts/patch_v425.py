#!/usr/bin/env python3
"""Patch v424 -> v425:
- Fix 500: revert huddle_members back to string array (backend rejects objects)
- Encode role as suffix instead: "borbie:admin", "username" (no suffix = normal)
- Update both normalisers to parse the role suffix so admin gets correct bird
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v424.js'
dst = '_deploy/assets/index-DUcNPOLc-v425.js'

content = open(src, encoding='utf-8').read()
errors = []

# Shared normaliser that handles:
#   old format:  "username"          -> role null
#   new format:  "username:admin"    -> role admin
#   new format:  "username:mod"      -> role mod
#   object (safety): {u,b,r}        -> passthrough
_NORM = (
    'const _normHm=_x=>{'
      'if(typeof _x!==`string`)return{username:_x.u||String(_x),browser_id:_x.b||null,role:_x.r||null};'
      'const _ci=_x.lastIndexOf(`:`);'
      'if(_ci>0){const _r=_x.slice(_ci+1);if(_r===`admin`||_r===`mod`)return{username:_x.slice(0,_ci),browser_id:null,role:_r};}'
      'return{username:_x,browser_id:null,role:null};'
    '};'
)

# ── 1. create-post: strings with optional ":role" suffix (backend safe) ───────
OLD_CREATE = 'huddle_members:_isHuddle?_hmTagged.map(_u=>({u:_u.username,b:_u.browser_id||null,r:_u.role||null})):[]'
NEW_CREATE  = 'huddle_members:_isHuddle?_hmTagged.map(_u=>_u.role?`${_u.username}:${_u.role}`:_u.username):[]'
if OLD_CREATE in content:
    content = content.replace(OLD_CREATE, NEW_CREATE, 1)
    print('OK: create-post encodes role suffix in string')
else:
    errors.append('FAIL: create-post huddle_members not found')

# ── 2. feed normaliser ────────────────────────────────────────────────────────
OLD_FEED_NORM = 'const _normHm=_x=>typeof _x===`string`?{username:_x,browser_id:null,role:null}:{username:_x.u||_x,browser_id:_x.b||null,role:_x.r||null};_fHm=_hm.filter(Boolean).map(_normHm)'
NEW_FEED_NORM = _NORM + '_fHm=_hm.filter(Boolean).map(_normHm)'
if OLD_FEED_NORM in content:
    content = content.replace(OLD_FEED_NORM, NEW_FEED_NORM, 1)
    print('OK: feed normaliser handles role suffix')
else:
    errors.append('FAIL: feed normaliser not found')

# ── 3. post page normaliser ───────────────────────────────────────────────────
OLD_PP_NORM = 'const _normHm=_x=>typeof _x===`string`?{username:_x,browser_id:null,role:null}:{username:_x.u||_x,browser_id:_x.b||null,role:_x.r||null};return _hm.map(_normHm)'
NEW_PP_NORM = _NORM + 'return _hm.map(_normHm)'
if OLD_PP_NORM in content:
    content = content.replace(OLD_PP_NORM, NEW_PP_NORM, 1)
    print('OK: post page normaliser handles role suffix')
else:
    errors.append('FAIL: post page normaliser not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
