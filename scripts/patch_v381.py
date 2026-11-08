#!/usr/bin/env python3
"""Patch v380 -> v381:
- Postcard (Ir) huddle body: compute member list live from e.huddle_members
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v380.js'
dst = '_deploy/assets/index-DUcNPOLc-v381.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '{text:f,attachment:p}=Mr(e.content);function m(e,t,n)'
NEW = (
    '{text:_rawF,attachment:p}=Mr(e.content);'
    'const f=(e.is_huddle||e.community_id===`feedback`)?(()=>{try{'
    'const _hm=JSON.parse(e.huddle_members||`[]`);'
    'return`Huddle with: ${[e.username,..._hm].filter(Boolean).join(`, `)}`'
    ';}catch(_){return _rawF;}})():_rawF;'
    'function m(e,t,n)'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: postcard huddle body uses live member list')
else:
    errors.append('FAIL: postcard body destructure not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
