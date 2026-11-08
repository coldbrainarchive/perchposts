#!/usr/bin/env python3
"""Patch v552 -> v553:
In Ur (new post), add a useEffect that fetches the role for an initially-invited
user (loaded from ?invite= URL param) so their pill shows the correct mod/admin colour.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v552.js'
dst = '_deploy/assets/index-DUcNPOLc-v553.js'

content = open(src, encoding='utf-8').read()
errors = []

ROLE_FETCH = (
    '(0,_.useEffect)(()=>{'
    'if(_hmTagged.length===1&&_hmTagged[0].role===null){'
    'const _iun=_hmTagged[0].username;'
    'fetch(`${R}/user-stats?username=${encodeURIComponent(_iun)}`)'
    '.then(r=>r.json())'
    '.then(d=>{if(d.role)_setHmTagged(prev=>prev.map(u=>u.username===_iun?{...u,role:d.role}:u));});'
    '}},[]);'
)

OLD = 'j=(0,_.useRef)(null);(0,_.useEffect)(()=>{function e(e){w.current&&'
NEW = 'j=(0,_.useRef)(null);' + ROLE_FETCH + '(0,_.useEffect)(()=>{function e(e){w.current&&'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: invite role fetch useEffect added to Ur')
else:
    errors.append('FAIL: Ur refs anchor not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
