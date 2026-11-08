#!/usr/bin/env python3
"""Patch v470 -> v472: Scale up the USER profile sidebar bird from sz=32 to
sz=56 to match the notification screen ratio (large bird above small pill)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v470.js'
dst = '_deploy/assets/index-DUcNPOLc-v472.js'

content = open(src, encoding='utf-8').read()
errors = []

# Admin bird container
OLD_ADM = 'style:{position:`relative`,display:`inline-block`,width:32,height:32,overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{position:`absolute`,height:36'
NEW_ADM = 'style:{position:`relative`,display:`inline-block`,width:56,height:56,overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{position:`absolute`,height:62'
if OLD_ADM in content:
    content = content.replace(OLD_ADM, NEW_ADM, 1)
    print('OK: admin bird 32→56')
else:
    errors.append('FAIL: admin bird container')

# Regular bird outer span
OLD_BIRD = 'style:{position:`relative`,display:`inline-block`,fontSize:32,lineHeight:1,width:`32px`,height:`32px`},children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display'
NEW_BIRD = 'style:{position:`relative`,display:`inline-block`,fontSize:56,lineHeight:1,width:`56px`,height:`56px`},children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display'
if OLD_BIRD in content:
    content = content.replace(OLD_BIRD, NEW_BIRD, 1)
    print('OK: regular bird 32→56')
else:
    errors.append('FAIL: regular bird span')

# _spEls size
OLD_SP = '_spEls(_bd.s,32)'
NEW_SP = '_spEls(_bd.s,56)'
if OLD_SP in content:
    content = content.replace(OLD_SP, NEW_SP, 1)
    print('OK: _spEls 32→56')
else:
    errors.append('FAIL: _spEls call')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
