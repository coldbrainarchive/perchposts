#!/usr/bin/env python3
"""Patch v185 -> v186: render polka-dot spots on the big bird in the notifications panel header."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v185.js'
dst = '_deploy/assets/index-DUcNPOLc-v186.js'

content = open(src, encoding='utf-8').read()
errors = []

# The big bird is currently a single-child jsx span with filter but no spots.
# Wrap it like Xn does: relative container + emoji span + _spEls overlay.
OLD = (
    '(0,L.jsx)(`span`,{style:{fontSize:56,lineHeight:1,'
    'filter:_bird&&_bird.f?_bird.f:``,display:`block`},'
    'children:_bird&&_bird.e?_bird.e:`🐤`})'
)
NEW = (
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,fontSize:56,lineHeight:1},'
    'children:['
    '(0,L.jsx)(`span`,{style:{filter:_bird&&_bird.f?_bird.f:``,display:`block`},children:_bird&&_bird.e?_bird.e:`🐤`}),'
    '...(_bird&&_bird.s?_spEls(_bird.s,56):[])'
    ']})'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: spots overlay added to big bird in notifications panel')
else:
    errors.append('FAIL: big bird span not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
