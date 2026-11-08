#!/usr/bin/env python3
"""Patch v342 -> v343:
- Restore te.current guard: only scroll to bottom when navigated via comment button
- View Post navigates without scrollToComments state so stays at top
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v342.js'
dst = '_deploy/assets/index-DUcNPOLc-v343.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'if(A.current||u.length===0)return;'
    'A.current=!0;'
    'if(history.scrollRestoration)history.scrollRestoration=`manual`;'
)
NEW = (
    'if(!te.current||A.current||u.length===0)return;'
    'A.current=!0;'
    'if(history.scrollRestoration)history.scrollRestoration=`manual`;'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: te.current guard restored — only scroll to bottom when coming from comment button')
else:
    errors.append('FAIL: scroll guard not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
