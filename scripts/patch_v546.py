#!/usr/bin/env python3
"""Patch v545 -> v546: Add both Huddle and See Posts buttons in the Bird overlay."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v545.js'
dst = '_deploy/assets/index-DUcNPOLc-v546.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_BTN = ('(0,L.jsx)(`div`,{style:{padding:`0 16px`,marginTop:8},'
           'children:(0,L.jsx)(`a`,{href:`/?user=${encodeURIComponent(e.username)}`,'
           'style:{display:`block`,textAlign:`center`,padding:`13px`,borderRadius:12,'
           'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:15,textDecoration:`none`},'
           'children:`See Posts`})})')

NEW_BTN = ('(0,L.jsxs)(`div`,{style:{padding:`0 16px`,marginTop:8,display:`flex`,gap:8},'
           'children:['
           '(0,L.jsx)(`a`,{href:`/new?huddle=1&invite=${encodeURIComponent(e.username)}`,'
           'style:{display:`block`,flex:1,textAlign:`center`,padding:`13px`,borderRadius:12,'
           'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:15,textDecoration:`none`},'
           'children:`Huddle`}),'
           '(0,L.jsx)(`a`,{href:`/?user=${encodeURIComponent(e.username)}`,'
           'style:{display:`block`,flex:1,textAlign:`center`,padding:`13px`,borderRadius:12,'
           'background:`#1e293b`,color:`#c084fc`,fontWeight:700,fontSize:15,textDecoration:`none`,'
           'border:`1.5px solid #c084fc`},'
           'children:`See Posts`})'
           ']})')

if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('OK: two buttons (Huddle + See Posts) added')
else:
    errors.append('FAIL: See Posts button container not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
