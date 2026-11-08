#!/usr/bin/env python3
"""Patch v379 -> v380:
- Huddle post page body: compute member list live from c.huddle_members instead of
  static c.content, so it updates instantly when members are added/removed
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v379.js'
dst = '_deploy/assets/index-DUcNPOLc-v380.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'let{text:e,attachment:t}=Mr(c.content);'
    'return(0,L.jsxs)(L.Fragment,{children:[(c.title||e)'
)
NEW = (
    'let{text:_rawE,attachment:t}=Mr(c.content);'
    'const e=c.is_huddle?(()=>{try{const _hm=JSON.parse(c.huddle_members||`[]`);'
    'return`Huddle with: ${[c.username,..._hm].filter(Boolean).join(`, `)}`;'
    '}catch(_){return _rawE;}})():_rawE;'
    'return(0,L.jsxs)(L.Fragment,{children:[(c.title||e)'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: huddle body renders live member list')
else:
    errors.append('FAIL: post body rendering not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
