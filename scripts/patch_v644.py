#!/usr/bin/env python3
"""Patch v643 -> v644:
Add maxHeight + objectFit:cover to video so portrait videos are capped in
height and cropped (not squished). Default maxH is 400 for posts, 240 for comments.
Also reduce default maxH from 400 to 320 for better mobile viewing.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v643.js'
dst = '_deploy/assets/index-DUcNPOLc-v644.js'

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

# Add maxHeight + objectFit:cover to video style
patch(
    'width:' + q + '100%' + q + ',borderRadius:10,display:' + q + 'block' + q + ',cursor:' + q + 'pointer' + q,
    'width:' + q + '100%' + q + ',maxHeight:_mh,objectFit:' + q + 'cover' + q + ',borderRadius:10,display:' + q + 'block' + q + ',cursor:' + q + 'pointer' + q,
    'video maxHeight + objectFit cover'
)

# Reduce default maxH from 400 to 320
patch(
    'function Fr({attachment:e,postId:o,maxH:_mh=400})',
    'function Fr({attachment:e,postId:o,maxH:_mh=320})',
    'reduce default maxH to 320'
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
