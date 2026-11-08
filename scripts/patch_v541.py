#!/usr/bin/env python3
"""Patch v540 -> v541: Fix _isHuddleBoard scope error — use u===feedback check directly."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v540.js'
dst = '_deploy/assets/index-DUcNPOLc-v541.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = ('_isHuddleBoard&&!localStorage.getItem(`auth_token`)&&(0,L.jsxs)(`div`,{')
NEW = ('(u===`feedback`||u===`huddles`)&&!localStorage.getItem(`auth_token`)&&(0,L.jsxs)(`div`,{')
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: replaced _isHuddleBoard with u===feedback check')
else:
    errors.append('FAIL: placeholder condition not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
