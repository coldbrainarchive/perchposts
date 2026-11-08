#!/usr/bin/env python3
"""Patch v430 -> v431:
Search-bar user chip background: also check _adminUsers (not just UR)
so the white background shows even before UR is loaded.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v430.js'
dst = '_deploy/assets/index-DUcNPOLc-v431.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = ('background:(()=>{const _ua=UR.find(_f=>_f.username.toLowerCase()===m.toLowerCase());'
       'if(_ua?.role===`admin`)_adminUsers.add(m.toLowerCase());'
       'return _ua?.role===`admin`;})()?`#ffffff`:Hn(null,m)')
NEW = ('background:(_adminUsers.has(m.toLowerCase())||(()=>{const _ua=UR.find(_f=>_f.username.toLowerCase()===m.toLowerCase());'
       'if(_ua?.role===`admin`)_adminUsers.add(m.toLowerCase());'
       'return _ua?.role===`admin`;})()?!0:!1)?`#ffffff`:Hn(null,m)')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: chip background checks _adminUsers first')
else:
    errors.append('FAIL: chip background not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
