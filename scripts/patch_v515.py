#!/usr/bin/env python3
"""Patch v514 -> v515: Fix mod purple in new post huddle Add Birds dropdown and tagged pills."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v514.js'
dst = '_deploy/assets/index-DUcNPOLc-v515.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. _hmTagR dropdown: fix background ──────────────────────────────────────
OLD_TAGR_BG = ('background:_u.role===`admin`?`#ffffff`:Hn(_u.browser_id||null,_u.username),'
               'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1,'
               'flexShrink:0,boxSizing:`border-box`},children:[(()=>{const _jd=Jn({username:_u.username,'
               'browser_id:_u.browser_id||null,is_admin:_u.role===`admin`})||{}')
NEW_TAGR_BG = ('background:_u.role===`admin`?`#ffffff`:_u.role===`mod`?`#c084fc`:Hn(_u.browser_id||null,_u.username),'
               'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1,'
               'flexShrink:0,boxSizing:`border-box`},children:[(()=>{const _jd=Jn({username:_u.username,'
               'browser_id:_u.browser_id||null,is_admin:_u.role===`admin`,is_mod:_u.role===`mod`})||{}')
if OLD_TAGR_BG in content:
    content = content.replace(OLD_TAGR_BG, NEW_TAGR_BG, 1)
    print('OK: _hmTagR dropdown background + Jn fixed')
else:
    errors.append('FAIL: _hmTagR dropdown pill not found')

# ── 2. _hmTagged pills: fix background (Jn already has is_mod from v512) ──────
OLD_TAGGED_BG = ('background:_u.role===`admin`?`#ffffff`:Hn(_u.browser_id||null,_u.username),'
                 'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1,'
                 'flexShrink:0,boxSizing:`border-box`},children:[(()=>{const _jd=Jn({username:_u.username,'
                 'browser_id:_u.browser_id||null,is_admin:_u.role===`admin`,is_mod:_u.role===`mod`})||{}')
NEW_TAGGED_BG = ('background:_u.role===`admin`?`#ffffff`:_u.role===`mod`?`#c084fc`:Hn(_u.browser_id||null,_u.username),'
                 'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,lineHeight:1,'
                 'flexShrink:0,boxSizing:`border-box`},children:[(()=>{const _jd=Jn({username:_u.username,'
                 'browser_id:_u.browser_id||null,is_admin:_u.role===`admin`,is_mod:_u.role===`mod`})||{}')
if OLD_TAGGED_BG in content:
    content = content.replace(OLD_TAGGED_BG, NEW_TAGGED_BG, 1)
    print('OK: _hmTagged pill background fixed')
else:
    errors.append('FAIL: _hmTagged pill background not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
