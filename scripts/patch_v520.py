#!/usr/bin/env python3
"""Patch v519 -> v520: Add globe badge to top-left of user card for mods (purple) and admins (white)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v519.js'
dst = '_deploy/assets/index-DUcNPOLc-v520.js'

content = open(src, encoding='utf-8').read()
errors = []

# The card's outer wrapper — add position:relative so we can absolutely position the globe
OLD_CARD = ('style:{background:`#161920`,borderRadius:14,border:`1px solid #2e303a`,overflow:`hidden`}')
NEW_CARD = ('style:{background:`#161920`,borderRadius:14,border:`1px solid #2e303a`,overflow:`hidden`,position:`relative`}')
if OLD_CARD in content:
    content = content.replace(OLD_CARD, NEW_CARD, 1)
    print('OK: card wrapper set to position:relative')
else:
    errors.append('FAIL: card wrapper style not found')

# Insert globe badge as first child of the card (before the USER/RANK flex row)
# The first child is the flex row div with display:flex,minHeight:100
OLD_ROW = ('children:[(0,L.jsxs)(`div`,{style:{display:`flex`,minHeight:100}')
NEW_ROW = ('children:[(_isAdmin||_isMod)&&(0,L.jsx)(`div`,{style:{position:`absolute`,top:8,left:10,zIndex:2},'
           'children:(0,L.jsxs)(`svg`,{width:16,height:16,viewBox:`0 0 100 100`,xmlns:`http://www.w3.org/2000/svg`,'
           'children:['
           '(0,L.jsx)(`circle`,{cx:50,cy:50,r:44,fill:`none`,stroke:_isAdmin?`#ffffff`:`#c084fc`,strokeWidth:7}),'
           '(0,L.jsx)(`line`,{x1:6,y1:50,x2:94,y2:50,stroke:_isAdmin?`#ffffff`:`#c084fc`,strokeWidth:6}),'
           '(0,L.jsx)(`path`,{d:`M 14 28 Q 50 38 86 28`,fill:`none`,stroke:_isAdmin?`#ffffff`:`#c084fc`,strokeWidth:6}),'
           '(0,L.jsx)(`path`,{d:`M 14 72 Q 50 62 86 72`,fill:`none`,stroke:_isAdmin?`#ffffff`:`#c084fc`,strokeWidth:6}),'
           '(0,L.jsx)(`ellipse`,{cx:50,cy:50,rx:16,ry:44,fill:`none`,stroke:_isAdmin?`#ffffff`:`#c084fc`,strokeWidth:6,clipPath:`url(#ucbc)`}),'
           '(0,L.jsx)(`ellipse`,{cx:50,cy:50,rx:32,ry:44,fill:`none`,stroke:_isAdmin?`#ffffff`:`#c084fc`,strokeWidth:6,clipPath:`url(#ucbc)`}),'
           '(0,L.jsx)(`clipPath`,{id:`ucbc`,children:(0,L.jsx)(`circle`,{cx:50,cy:50,r:44})})'
           ']})})'
           ',(0,L.jsxs)(`div`,{style:{display:`flex`,minHeight:100}')
if OLD_ROW in content:
    content = content.replace(OLD_ROW, NEW_ROW, 1)
    print('OK: globe badge added to user card')
else:
    errors.append('FAIL: user card first child row not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
