#!/usr/bin/env python3
"""Patch v384 -> v385:
- New post page (Ur): swipe left from left edge navigates back (saves scroll position)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v384.js'
dst = '_deploy/assets/index-DUcNPOLc-v385.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'oe=sr(h)||nr[0];return(0,L.jsx)(`div`,{className:`home-shell`'
NEW = (
    'oe=sr(h)||nr[0];'
    '(0,_.useEffect)(()=>{'
    'let _sx=0,_sy=0;'
    'const _ts=e=>{_sx=e.touches[0].clientX;_sy=e.touches[0].clientY;};'
    'const _te=e=>{'
    'const _dx=e.changedTouches[0].clientX-_sx;'
    'const _dy=e.changedTouches[0].clientY-_sy;'
    'if(_sx<50&&_dx>60&&Math.abs(_dx)>Math.abs(_dy)*1.5)r(-1);'
    '};'
    'document.addEventListener(`touchstart`,_ts,{passive:!0});'
    'document.addEventListener(`touchend`,_te,{passive:!0});'
    'return()=>{document.removeEventListener(`touchstart`,_ts);document.removeEventListener(`touchend`,_te);};'
    '},[]);'
    'return(0,L.jsx)(`div`,{className:`home-shell`'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: swipe-left added to new post page')
else:
    errors.append('FAIL: Ur return anchor not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
