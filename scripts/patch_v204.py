#!/usr/bin/env python3
"""Patch v203 -> v204: show loading state below URL input while link is being fetched."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v203.js'
dst = '_deploy/assets/index-DUcNPOLc-v204.js'

content = open(src, encoding='utf-8').read()
errors = []

# After the URL input row, insert an A&&(...) loading indicator.
# The URL row ends just before the file inputs.
OLD = (
    'children:A?`…`:`Add`})]}),(0,L.jsx)(`input`,{ref:ie,type:`file`'
)
NEW = (
    'children:A?`…`:`Add`})]),'
    'A&&(0,L.jsx)(`div`,{style:{textAlign:`center`,padding:`10px 0 2px`,'
    'color:`#94a3b8`,fontSize:13},children:`Fetching link preview…`})'
    ']}),(0,L.jsx)(`input`,{ref:ie,type:`file`'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: link loading indicator added')
else:
    errors.append('FAIL: URL input row end not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
