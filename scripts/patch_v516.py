#!/usr/bin/env python3
"""Patch v515 -> v516: Fix selected invite pill colour for mods."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v515.js'
dst = '_deploy/assets/index-DUcNPOLc-v516.js'

content = open(src, encoding='utf-8').read()
errors = []

# Fix selected _wpInvP pill background + Jn is_mod
OLD = ('_wpInvP.role===`admin`?`#ffffff`:Hn(_wpInvP.browser_id||null,_wpInvP.username),'
       'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1},'
       'children:[(()=>{const _jd=Jn({username:_wpInvP.username,'
       'browser_id:_wpInvP.browser_id||null,is_admin:_wpInvP.role===`admin`})||{}')
NEW = ('_wpInvP.role===`admin`?`#ffffff`:_wpInvP.role===`mod`?`#c084fc`:Hn(_wpInvP.browser_id||null,_wpInvP.username),'
       'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1},'
       'children:[(()=>{const _jd=Jn({username:_wpInvP.username,'
       'browser_id:_wpInvP.browser_id||null,is_admin:_wpInvP.role===`admin`,is_mod:_wpInvP.role===`mod`})||{}')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: selected invite pill background fixed for mods')
else:
    errors.append('FAIL: _wpInvP pill background not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
