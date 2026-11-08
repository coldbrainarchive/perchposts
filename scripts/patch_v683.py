#!/usr/bin/env python3
"""Patch v682 -> v683:
Preload all images when the lightbox opens so swiping/clicking to the next photo
is instant instead of waiting for a network fetch each time.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v682.js'
dst = '_deploy/assets/index-DUcNPOLc-v683.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append('FAIL (' + label + '): not found')
    elif n > 1:
        errors.append('FAIL (' + label + '): ' + str(n) + ' matches')
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

for var in ['_pAtts', '_cAtts', '_tAtts']:
    old = ('document.body.appendChild(_ov);}}),'+var+'.length>1&&')
    new = ('document.body.appendChild(_ov);'
           + f'{var}.forEach(_a=>{{new Image().src=_a.url;}});'
           + '}}),'+var+'.length>1&&')
    patch(old, new, f'{var}: preload all images on lightbox open')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print('Paren delta: ' + str(p_delta) + ', Brace delta: ' + str(b_delta))
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
