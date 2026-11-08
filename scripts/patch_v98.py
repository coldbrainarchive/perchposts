#!/usr/bin/env python3
"""Patch v97 -> v98: make bird pill match input field size with valid CSS colors."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v97.js'
dst = '_deploy/assets/index-DUcNPOLc-v98.js'

content = open(src, encoding='utf-8').read()
errors = []

# Extract the BIRD_GEN IIFE verbatim from the file
iife_start = content.find('(function(){var _a=["african"')
iife_end   = content.find('})()', iife_start) + 4
BIRD_GEN   = content[iife_start:iife_end]

# Build the old block marker (start and end anchors)
OLD_START = 'C?(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,justifyContent:`center`,gap:8}'
OLD_END   = ':(0,L.jsx)(`input`,{placeholder:`Username`'

idx = content.find(OLD_START)
end_idx = content.find(OLD_END, idx)

if idx == -1:
    errors.append('FAIL: old signup block start not found')
elif end_idx == -1:
    errors.append('FAIL: old signup block end not found')
else:
    OLD_BLOCK = content[idx:end_idx]

    # New block: single div sized like the form inputs, valid CSS colors
    NEW_BLOCK = (
        'C?(0,L.jsxs)(`div`,{'
        'onClick:function(){_su(' + BIRD_GEN + ')},'
        'style:{'
          'display:`flex`,'
          'alignItems:`center`,'
          'gap:8,'
          'padding:`9px 12px`,'
          'borderRadius:10,'
          'border:_gu?`1.5px solid ${Hn(null,_gu)}`:`1.5px dashed #3f4756`,'
          "background:_gu?Hn(null,_gu).replace('hsl(','hsla(').replace(')',', 0.12)'):`transparent`,"
          'cursor:`pointer`,'
          'userSelect:`none`,'
          'boxSizing:`border-box`,'
          'width:`100%`,'
        '},'
        'children:['
          '(0,L.jsx)(`span`,{style:{fontSize:18},children:`\U0001f424`}),'
          '(0,L.jsx)(`span`,{style:{flex:1,fontSize:14,fontWeight:700,'
            'color:_gu?Hn(null,_gu):`#64748b`,'
            'letterSpacing:`-0.01em`,'
            'overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`'
          '},children:_gu||`tap to generate username`})'
        ']})'
    )

    content = content[:idx] + NEW_BLOCK + content[end_idx:]
    print(f'OK: replaced signup block ({len(OLD_BLOCK)} -> {len(NEW_BLOCK)} chars)')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
