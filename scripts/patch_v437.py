#!/usr/bin/env python3
"""Patch v436 -> v437:
Make huddle member pills in the post body clickable — navigate to /?user=username
just like the OP pill at the top of the post page.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v436.js'
dst = '_deploy/assets/index-DUcNPOLc-v437.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'e.map(_u=>(0,L.jsx)(Xn,{record:{username:_u.username,browser_id:_u.browser_id,is_admin:_u.role===`admin`},name:_u.username,color:Hn(_u.browser_id,_u.username)},_u.username))'
NEW = 'e.map(_u=>(0,L.jsx)(Xn,{record:{username:_u.username,browser_id:_u.browser_id,is_admin:_u.role===`admin`},name:_u.username,color:Hn(_u.browser_id,_u.username),onClick:_u.username?()=>o(`/?user=${encodeURIComponent(_u.username)}`):void 0},_u.username))'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: huddle member pills are now clickable')
else:
    errors.append('FAIL: member pills render not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
