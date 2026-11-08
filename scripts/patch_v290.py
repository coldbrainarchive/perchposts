#!/usr/bin/env python3
"""Patch v289 -> v290: time filter column (Hour/Day) stacks vertically —
add flexDirection:column to override search-column's flex-wrap:wrap."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v289.js'
dst = '_deploy/assets/index-DUcNPOLc-v290.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_TIME_COL = (
    'className:`search-column`,style:{borderLeft:`1px solid #374151`,'
    'minWidth:0,overflow:`hidden`,gridColumn:C?`auto`:`1 / -1`}'
)
NEW_TIME_COL = (
    'className:`search-column`,style:{borderLeft:`1px solid #374151`,'
    'minWidth:0,overflow:`hidden`,gridColumn:C?`auto`:`1 / -1`,'
    'flexDirection:`column`,alignItems:`stretch`,gap:4}'
)

if OLD_TIME_COL in content:
    content = content.replace(OLD_TIME_COL, NEW_TIME_COL, 1)
    print('OK: time filter column set to flex-direction:column')
else:
    errors.append('FAIL: time filter column style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
