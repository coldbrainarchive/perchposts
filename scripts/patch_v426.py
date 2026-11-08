#!/usr/bin/env python3
"""Patch v425 -> v426:
Search-bar user chip: apply the same CSS filter (hue-rotate/saturation/brightness)
to the bird emoji that Xn and _UserCard apply, so all three match.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v425.js'
dst = '_deploy/assets/index-DUcNPOLc-v426.js'

content = open(src, encoding='utf-8').read()
errors = []

# The chip currently renders the bird emoji with no filter
OLD_CHIP = ':(0,L.jsx)(`span`,{children:(Jn({username:m,browser_id:null})||{}).e||`🐦`})'
# Apply the CSS filter from Jn result so it matches Xn / _UserCard
NEW_CHIP = ':(()=>{const _jd=Jn({username:m,browser_id:null})||{};return(0,L.jsx)(`span`,{style:{filter:_jd.f||``},children:_jd.e||`🐦`});})()'
if OLD_CHIP in content:
    content = content.replace(OLD_CHIP, NEW_CHIP, 1)
    print('OK: search-bar user chip applies CSS filter to bird emoji')
else:
    errors.append('FAIL: chip bird span not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
