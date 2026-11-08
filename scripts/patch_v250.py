#!/usr/bin/env python3
"""Patch v249 -> v250: remove bottom border on UserCard, smaller admin bird, white admin pill."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v249.js'
dst = '_deploy/assets/index-DUcNPOLc-v250.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove borderBottom from outer _UserCard wrapper ──────────────────────
OLD_OUTER = 'padding:`10px 14px`,borderBottom:`1px solid #2e303a`}'
NEW_OUTER = 'padding:`10px 14px`}'
if OLD_OUTER in content:
    content = content.replace(OLD_OUTER, NEW_OUTER, 1)
    print('OK: borderBottom removed from UserCard wrapper')
else:
    errors.append('FAIL: outer borderBottom not found')

# ── 2. Make admin bird image smaller ─────────────────────────────────────────
OLD_BIRD = 'height:54,width:`auto`,bottom:0,left:`50%`,transform:`translateX(-50%)`'
NEW_BIRD = 'height:36,width:`auto`,bottom:0,left:`50%`,transform:`translateX(-50%)`'
if OLD_BIRD in content:
    content = content.replace(OLD_BIRD, NEW_BIRD, 1)
    print('OK: admin bird height reduced to 36')
else:
    errors.append('FAIL: admin bird height not found')

# ── 3. White username pill for admin (hat = admin) ────────────────────────────
OLD_PILL = 'background:_col,borderColor:_col,cursor:`default`,maxWidth:150'
NEW_PILL = 'background:_bd&&_bd.hat?`#ffffff`:_col,borderColor:_bd&&_bd.hat?`#e2e8f0`:_col,cursor:`default`,maxWidth:150'
if OLD_PILL in content:
    content = content.replace(OLD_PILL, NEW_PILL, 1)
    print('OK: admin username pill set to white')
else:
    errors.append('FAIL: username pill color not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
