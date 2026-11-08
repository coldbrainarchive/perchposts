#!/usr/bin/env python3
"""Patch v547 -> v548:
- Restore _UserCard internal Huddle button but guard with _om so it only
  shows when an onMessage handler is provided (Bird Info page), not in the
  comment overlay where _om is undefined.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v547.js'
dst = '_deploy/assets/index-DUcNPOLc-v548.js'

content = open(src, encoding='utf-8').read()
errors = []

# Find the closing of the _UserCard return — the worms cell ends the stats row,
# then we need to re-insert the Huddle button before the closing brackets.
# We look for the unique spot just before _UserCard's closing.
OLD_CLOSE = ('(0,L.jsx)(`div`,{style:{fontSize:13,color:`#f1f5f9`,fontWeight:700,'
             'textAlign:`center`,width:`100%`},children:_wc})]})]})]})')
NEW_CLOSE = ('(0,L.jsx)(`div`,{style:{fontSize:13,color:`#f1f5f9`,fontWeight:700,'
             'textAlign:`center`,width:`100%`},children:_wc})]})]}),'
             '_om&&_me&&_me!==_un&&(0,L.jsx)(`button`,{onClick:()=>_om(_un,_br),'
             'style:{width:`100%`,marginTop:8,padding:`11px`,borderRadius:12,'
             'border:`1px solid #2e303a`,background:`#161920`,color:`#c084fc`,'
             'fontWeight:700,fontSize:15,cursor:`pointer`},children:`Huddle`})'
             ']})')
if OLD_CLOSE in content:
    content = content.replace(OLD_CLOSE, NEW_CLOSE, 1)
    print('OK: _UserCard Huddle button restored with _om guard')
else:
    errors.append('FAIL: _UserCard closing not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
