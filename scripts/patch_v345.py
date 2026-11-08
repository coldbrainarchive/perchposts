#!/usr/bin/env python3
"""Patch v344 -> v345: show subtle 'No chirps yet' placeholder when chat-window is empty."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v344.js'
dst = '_deploy/assets/index-DUcNPOLc-v345.js'

content = open(src, encoding='utf-8').read()
errors = []

# Change children:de.map(...) to children:[placeholder,...de.map(...)]
# Step 1: wrap the map in an array with a spread, add placeholder before it
OLD_OPEN = (
    'children:de.map(e=>(0,L.jsx)(Rr,{comment:e,postBrowserId:c.browser_id,postUsername:c.username||null,myUsername:n,'
)
NEW_OPEN = (
    'children:[de.length===0&&(0,L.jsx)(`p`,{style:{textAlign:`center`,color:`rgba(148,163,184,0.3)`,fontSize:13,padding:`16px 0`,margin:0},children:`No chirps yet`}),'
    '...de.map(e=>(0,L.jsx)(Rr,{comment:e,postBrowserId:c.browser_id,postUsername:c.username||null,myUsername:n,'
)
if OLD_OPEN in content:
    content = content.replace(OLD_OPEN, NEW_OPEN, 1)
    print('OK: placeholder + spread prefix added')
else:
    errors.append('FAIL: chat-window children map open not found')

# Step 2: close the array after the map — insert ] between ))  and }),!c.locked
OLD_CLOSE = '},e.id))}),!c.locked'
NEW_CLOSE = '},e.id))]}),!c.locked'
if OLD_CLOSE in content:
    content = content.replace(OLD_CLOSE, NEW_CLOSE, 1)
    print('OK: closing ] added for children array')
else:
    errors.append('FAIL: chat-window map close not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
