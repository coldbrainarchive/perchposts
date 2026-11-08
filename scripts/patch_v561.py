#!/usr/bin/env python3
"""Patch v560 -> v561:
Postcard board-group spans have inline flexWrap:'wrap' overriding the CSS fix.
Change inline styles to nowrap+overflow:hidden so the last-tag collapse works.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v560.js'
dst = '_deploy/assets/index-DUcNPOLc-v561.js'

content = open(src, encoding='utf-8').read()
errors = []

# Feed postcard: style:{flexWrap:`wrap`,gap:5}
OLD1 = 'className:`feed-post-board-group`,style:{flexWrap:`wrap`,gap:5}'
NEW1 = 'className:`feed-post-board-group`,style:{flexWrap:`nowrap`,overflow:`hidden`,gap:5}'
if OLD1 in content:
    n = content.count(OLD1)
    content = content.replace(OLD1, NEW1)
    print(f'OK: fixed flexWrap:wrap gap:5 ({n} instances)')
else:
    errors.append('FAIL: flexWrap:wrap gap:5 not found')

# Post-detail / new-post postcard: style:{gap:6,flexWrap:`wrap`}
OLD2 = 'className:`feed-post-board-group`,style:{gap:6,flexWrap:`wrap`}'
NEW2 = 'className:`feed-post-board-group`,style:{gap:6,flexWrap:`nowrap`,overflow:`hidden`}'
if OLD2 in content:
    n = content.count(OLD2)
    content = content.replace(OLD2, NEW2)
    print(f'OK: fixed gap:6 flexWrap:wrap ({n} instances)')
else:
    errors.append('FAIL: gap:6 flexWrap:wrap not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
