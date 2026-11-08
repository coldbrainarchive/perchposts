#!/usr/bin/env python3
"""Patch v627 -> v629:
Fix video postcard squish: replace maxWidth+maxHeight with width:100% so the
video always fills the full card width at its natural aspect ratio.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v627.js'
dst = '_deploy/assets/index-DUcNPOLc-v629.js'

content = open(src, encoding='utf-8').read()
errors = []
q = chr(0x60)

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

# Replace maxWidth+maxHeight with width:100% (no height constraint = natural aspect ratio)
patch(
    'maxWidth:' + q + '100%' + q + ',borderRadius:10,maxHeight:_mh,display:' + q + 'block' + q + ',cursor:' + q + 'pointer' + q,
    'width:' + q + '100%' + q + ',borderRadius:10,display:' + q + 'block' + q + ',cursor:' + q + 'pointer' + q,
    'video width:100% fills card, natural aspect ratio'
)

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
