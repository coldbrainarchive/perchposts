#!/usr/bin/env python3
"""Patch v530 -> v531: Switch Nest columns from alignItems:center to alignItems:stretch
so text-align:center works on full-width divs instead of shrunk ones."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v530.js'
dst = '_deploy/assets/index-DUcNPOLc-v531.js'

content = open(src, encoding='utf-8').read()
errors = []

# Nest columns only - remove alignItems:center (let it default to stretch)
OLD_COLN = ('flex:1,minWidth:0,display:`flex`,flexDirection:`column`,alignItems:`center`,'
            'justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`')
NEW_COLN = ('flex:1,minWidth:0,display:`flex`,flexDirection:`column`,'
            'justifyContent:`center`,textAlign:`center`,gap:4,padding:`12px 8px`')
count = content.count(OLD_COLN)
if count > 0:
    content = content.replace(OLD_COLN, NEW_COLN)
    print(f'OK: Nest columns use stretch+textAlign:center ({count})')
else:
    errors.append('FAIL: Nest COLN not found')

# User card columns - same fix
OLD_COL = ('flex:1,minWidth:0,display:`flex`,flexDirection:`column`,alignItems:`center`,'
           'justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`')
NEW_COL = ('flex:1,minWidth:0,display:`flex`,flexDirection:`column`,'
           'justifyContent:`center`,textAlign:`center`,gap:4,padding:`10px 8px`')
count = content.count(OLD_COL)
if count > 0:
    content = content.replace(OLD_COL, NEW_COL)
    print(f'OK: user card columns use stretch+textAlign:center ({count})')
else:
    errors.append('FAIL: user card COL not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
