#!/usr/bin/env python3
"""Patch v337 -> v338: Find scrolls to TOP of parent comment instead of centering it."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v337.js'
dst = '_deploy/assets/index-DUcNPOLc-v338.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'if(t&&n){let e=n.offsetTop-t.clientHeight/2+n.offsetHeight/2;'
    't.scrollTo({top:e,behavior:`smooth`});'
)
NEW = (
    'if(t&&n){let e=n.offsetTop;'
    't.scrollTo({top:e,behavior:`smooth`});'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Find scrolls to top of parent comment')
else:
    errors.append('FAIL: Find scroll logic not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
