#!/usr/bin/env python3
"""Patch v473 -> v474: Both USER and RANK sections at 56px emoji size."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v473.js'
dst = '_deploy/assets/index-DUcNPOLc-v474.js'

content = open(src, encoding='utf-8').read()
errors = []

# User bird: 32→56
OLD_ADM = 'width:32,height:32,overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{position:`absolute`,height:36'
NEW_ADM = 'width:56,height:56,overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{position:`absolute`,height:62'
if OLD_ADM in content:
    content = content.replace(OLD_ADM, NEW_ADM, 1)
    print('OK: user admin bird 32→56')
else:
    errors.append('FAIL: user admin bird')

OLD_BIRD = 'fontSize:32,lineHeight:1,width:`32px`,height:`32px`'
NEW_BIRD = 'fontSize:56,lineHeight:1,width:`56px`,height:`56px`'
if OLD_BIRD in content:
    content = content.replace(OLD_BIRD, NEW_BIRD, 1)
    print('OK: user regular bird 32→56')
else:
    errors.append('FAIL: user regular bird')

if '_spEls(_bd.s,32)' in content:
    content = content.replace('_spEls(_bd.s,32)', '_spEls(_bd.s,56)', 1)
    print('OK: user _spEls 32→56')
else:
    errors.append('FAIL: user _spEls')

# Rank emoji: fontSize:32→56
OLD_RK = 'children:`RANK`}),(0,L.jsx)(`span`,{style:{fontSize:32,lineHeight:1},children:_rk?_rk.e:`🐣`})'
NEW_RK = 'children:`RANK`}),(0,L.jsx)(`span`,{style:{fontSize:56,lineHeight:1},children:_rk?_rk.e:`🐣`})'
if OLD_RK in content:
    content = content.replace(OLD_RK, NEW_RK, 1)
    print('OK: rank emoji 32→56')
else:
    errors.append('FAIL: rank emoji')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
