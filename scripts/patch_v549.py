#!/usr/bin/env python3
"""Patch v548 -> v549: Style the _UserCard Huddle button to match the overlay version."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v548.js'
dst = '_deploy/assets/index-DUcNPOLc-v549.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_BTN = ('_om&&_me&&_me!==_un&&(0,L.jsx)(`button`,{onClick:()=>_om(_un,_br),'
           'style:{width:`100%`,marginTop:8,padding:`11px`,borderRadius:12,'
           'border:`1px solid #2e303a`,background:`#161920`,color:`#c084fc`,'
           'fontWeight:700,fontSize:15,cursor:`pointer`},children:`Huddle`})')
NEW_BTN = ('_om&&_me&&_me!==_un&&(0,L.jsx)(`button`,{onClick:()=>_om(_un,_br),'
           'style:{width:`100%`,marginTop:8,padding:`13px`,borderRadius:12,'
           'border:`none`,background:`#c084fc`,color:`#14081d`,'
           'fontWeight:700,fontSize:15,cursor:`pointer`},children:`Huddle`})')

if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: _UserCard Huddle button styled to match overlay')
else:
    errors.append('FAIL: _UserCard Huddle button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
