#!/usr/bin/env python3
"""Patch v136 -> v137: tighter blob offsets + saturate/brightness variation."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v136.js'
dst = '_deploy/assets/index-DUcNPOLc-v137.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_FILTER = (
    "_f=`hue-rotate(${_a%360}deg)`;"
    "if(_a%3!==0){var _h1=(_a*7+137)%360,_h2=(_a*13+251)%360,"
    "_ox1=((_a>>4)%5)+2,_oy1=-((_a>>7)%5)-2,"
    "_ox2=-((_a>>10)%4)-1,_oy2=((_a>>13)%4)+2;"
    "if(_a%3===1)_f+=` drop-shadow(${_ox1}px ${_oy1}px 0px hsl(${_h1},90%,58%))`;"
    "else _f+=` drop-shadow(${_ox1}px ${_oy1}px 0px hsl(${_h1},90%,58%))"
    " drop-shadow(${_ox2}px ${_oy2}px 0px hsl(${_h2},90%,58%))`;}"
)

# Tighter offsets: 1-2px, soft 1px blur, added saturate+brightness for variety
NEW_FILTER = (
    "_sat=(_a>>5)%40+80,_bri=(_a>>8)%20+92,"
    "_f=`hue-rotate(${_a%360}deg) saturate(${_sat}%) brightness(${_bri}%)`;"
    "if(_a%3!==0){var _h1=(_a*7+137)%360,_h2=(_a*13+251)%360,"
    "_ox1=((_a>>4)%2)+1,_oy1=-((_a>>7)%2)-1,"
    "_ox2=-((_a>>10)%2),_oy2=((_a>>13)%2)+1;"
    "if(_a%3===1)_f+=` drop-shadow(${_ox1}px ${_oy1}px 1px hsl(${_h1},85%,62%))`;"
    "else _f+=` drop-shadow(${_ox1}px ${_oy1}px 1px hsl(${_h1},85%,62%))"
    " drop-shadow(${_ox2}px ${_oy2}px 1px hsl(${_h2},85%,62%))`;}"
)

count = content.count(OLD_FILTER)
if count > 0:
    content = content.replace(OLD_FILTER, NEW_FILTER)
    print(f'OK: updated {count} filter block(s) — tighter blobs + sat/brightness')
else:
    errors.append('FAIL: filter block not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
