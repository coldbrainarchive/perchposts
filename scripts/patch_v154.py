#!/usr/bin/env python3
"""Patch v153 -> v154: centre badge via inline style on the pill span itself."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v153.js'
dst = '_deploy/assets/index-DUcNPOLc-v154.js'

content = open(src, encoding='utf-8').read()
errors = []

# All CSS/media-query attempts are losing to blockification or specificity.
# Inline style on the span wins unconditionally.
# width:fit-content keeps the pill tight to its content at every viewport size.
# justifyContent:center centres the badge when it's the only visible child.
OLD_PILL_STYLE = (
    'return(0,L.jsxs)(`span`,{className:`user-pill`,style:{color:N?`#ffffff`:`#0a0a0a`,'
    'background:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:c,'
    'borderColor:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:c,'
    'cursor:r?`pointer`:`default`},'
)
NEW_PILL_STYLE = (
    'return(0,L.jsxs)(`span`,{className:`user-pill`,style:{color:N?`#ffffff`:`#0a0a0a`,'
    'background:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:c,'
    'borderColor:o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:c,'
    'cursor:r?`pointer`:`default`,'
    'justifyContent:`center`,width:`fit-content`},'
)

if OLD_PILL_STYLE in content:
    content = content.replace(OLD_PILL_STYLE, NEW_PILL_STYLE, 1)
    print('OK: pill inline style gets justifyContent:center + width:fit-content')
else:
    errors.append('FAIL: Xn pill style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
