#!/usr/bin/env python3
"""Patch v402 -> v403: pull wing emoji and count closer together (marginRight: -2px)"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v402.js'
dst = '_deploy/assets/index-DUcNPOLc-v403.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = '{style:{fontSize:14,lineHeight:1,display:`inline-flex`,alignItems:`center`,verticalAlign:`middle`},children:`\U0001fabd`}'
NEW = '{style:{fontSize:14,lineHeight:1,display:`inline-flex`,alignItems:`center`,verticalAlign:`middle`,marginRight:-3},children:`\U0001fabd`}'

count = content.count(OLD)
if count == 2:
    content = content.replace(OLD, NEW)
    print(f'OK: tightened gap in {count} like buttons')
else:
    errors.append(f'FAIL: expected 2, found {count}')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
