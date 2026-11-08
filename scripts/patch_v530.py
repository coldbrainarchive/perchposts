#!/usr/bin/env python3
"""Patch v529 -> v530: Add minWidth:0 to all columns so flex:1 enforces equal widths."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v529.js'
dst = '_deploy/assets/index-DUcNPOLc-v530.js'

content = open(src, encoding='utf-8').read()
errors = []

# User card columns
OLD_COL = ('flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,'
           'justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`')
NEW_COL = ('flex:1,minWidth:0,display:`flex`,flexDirection:`column`,alignItems:`center`,'
           'justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`')
count = content.count(OLD_COL)
if count > 0:
    content = content.replace(OLD_COL, NEW_COL)
    print(f'OK: minWidth:0 added to user card columns ({count})')
else:
    errors.append('FAIL: user card COL not found')

# Nest columns
OLD_COLN = ('flex:1,display:`flex`,flexDirection:`column`,alignItems:`center`,'
            'justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`')
NEW_COLN = ('flex:1,minWidth:0,display:`flex`,flexDirection:`column`,alignItems:`center`,'
            'justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`')
count = content.count(OLD_COLN)
if count > 0:
    content = content.replace(OLD_COLN, NEW_COLN)
    print(f'OK: minWidth:0 added to Nest columns ({count})')
else:
    errors.append('FAIL: Nest COLN not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
