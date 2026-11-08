#!/usr/bin/env python3
"""Patch v394 -> v395: show notification count instead of "Notifications" label"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v394.js'
dst = '_deploy/assets/index-DUcNPOLc-v395.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'children:`Notifications`'
NEW = 'children:j.length'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: label shows notification count')
else:
    errors.append('FAIL: Notifications label not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
