#!/usr/bin/env python3
"""Patch v472 -> v473: User bird 56→32 to match rank emoji size (fontSize:32)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v472.js'
dst = '_deploy/assets/index-DUcNPOLc-v473.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_ADM = 'width:56,height:56,overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{position:`absolute`,height:62'
NEW_ADM = 'width:32,height:32,overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{position:`absolute`,height:36'
if OLD_ADM in content:
    content = content.replace(OLD_ADM, NEW_ADM, 1)
    print('OK: admin bird 56→32')
else:
    errors.append('FAIL: admin bird')

OLD_BIRD = 'fontSize:56,lineHeight:1,width:`56px`,height:`56px`'
NEW_BIRD = 'fontSize:32,lineHeight:1,width:`32px`,height:`32px`'
if OLD_BIRD in content:
    content = content.replace(OLD_BIRD, NEW_BIRD, 1)
    print('OK: regular bird 56→32')
else:
    errors.append('FAIL: regular bird')

OLD_SP = '_spEls(_bd.s,56)'
NEW_SP = '_spEls(_bd.s,32)'
if OLD_SP in content:
    content = content.replace(OLD_SP, NEW_SP, 1)
    print('OK: _spEls 56→32')
else:
    errors.append('FAIL: _spEls')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
