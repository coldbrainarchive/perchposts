#!/usr/bin/env python3
"""Patch v157 -> v158: replace back button in link preview with 'Tap to close'."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v157.js'
dst = '_deploy/assets/index-DUcNPOLc-v158.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_HEADER = (
    '(0,L.jsx)(`div`,{style:{display:`flex`,alignItems:`center`,'
    'padding:`20px 20px 14px`,flexShrink:0},'
    'children:(0,L.jsx)(`button`,{type:`button`,onClick:l,'
    'style:{display:`inline-flex`,alignItems:`center`,justifyContent:`center`,'
    'width:26,height:26,borderRadius:999,border:`none`,background:`#20262f`,'
    'color:`#dbe4ee`,fontSize:12,fontWeight:800,cursor:`pointer`,flexShrink:0},'
    'children:`←`})})'
)
NEW_HEADER = (
    '(0,L.jsx)(`div`,{style:{display:`flex`,alignItems:`center`,'
    'justifyContent:`center`,padding:`14px 20px 8px`,flexShrink:0},'
    'children:(0,L.jsx)(`span`,{style:{fontSize:11,color:`#64748b`,'
    'letterSpacing:`0.04em`,fontWeight:500},children:`Tap to close`})})'
)

if OLD_HEADER in content:
    content = content.replace(OLD_HEADER, NEW_HEADER, 1)
    print('OK: back button replaced with centred "Tap to close"')
else:
    errors.append('FAIL: link preview header not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
