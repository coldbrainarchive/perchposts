#!/usr/bin/env python3
"""Patch v240 -> v241: fix missing ) closing thread header div in inbox JSX."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v240.js'
dst = '_deploy/assets/index-DUcNPOLc-v241.js'

content = open(src, encoding='utf-8').read()
errors = []

# Thread header div (0,L.jsxs)(`div`,{...children:[back_btn,span]}) is missing its closing )
# children:_dmThread}  closes span props
# )                    closes (0,L.jsx)( for span
# ]                    closes header children:[
# }                    closes header div props
# ← missing ) here to close (0,L.jsxs)( for header div
# ,                    separator to msgs div
OLD = 'children:_dmThread})]},(0,L.jsx)(`div`,{style:{flex:1'
NEW = 'children:_dmThread})]),(0,L.jsx)(`div`,{style:{flex:1'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: header div closing ) added')
else:
    errors.append('FAIL: header div end not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

# Verify fix
opens = content.count('(')
closes = content.count(')')
print(f'Paren balance: opens={opens}, closes={closes}, diff={opens-closes}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
