#!/usr/bin/env python3
"""Patch v448 -> v449:
Fix cursor-jumping bug in main search input:
onKeyDown checks stale React state `n` for backspace handling.
Use e.target.value (current DOM value) instead so it's always accurate.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v448.js'
dst = '_deploy/assets/index-DUcNPOLc-v449.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'e.key===`Escape`&&(a(!1),s(null)),e.key===`Backspace`&&!n&&(q2?ae():m?re():p?ne():f?te():d&&A())'
NEW = 'e.key===`Escape`&&(a(!1),s(null)),e.key===`Backspace`&&!e.target.value&&(q2?ae():m?re():p?ne():f?te():d&&A())'
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: backspace uses e.target.value (not stale n state)')
else:
    errors.append('FAIL: onKeyDown handler not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
