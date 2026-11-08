#!/usr/bin/env python3
"""Patch v397 -> v398: hide entire header div (not just button) when _showClear is false, eliminating the gap"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v397.js'
dst = '_deploy/assets/index-DUcNPOLc-v398.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'c===`notifications`&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,'
    'justifyContent:`space-between`,padding:`10px 16px 6px`,flexShrink:0,'
    'borderBottom:`1px solid rgba(255,255,255,0.06)`},'
)
NEW = (
    '_showClear&&c===`notifications`&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,'
    'justifyContent:`space-between`,padding:`10px 16px 6px`,flexShrink:0,'
    'borderBottom:`1px solid rgba(255,255,255,0.06)`},'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: header div hidden when _showClear is false')
else:
    errors.append('FAIL: header div not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
