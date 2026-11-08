#!/usr/bin/env python3
"""Patch v621 -> v623: thumbnail minHeight 120->160. No other changes.
The flex card uses alignItems:stretch so the thumbnail naturally grows with text,
but minHeight:160 guarantees a tall enough card even with minimal body text.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v621.js'
dst = '_deploy/assets/index-DUcNPOLc-v623.js'

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

# Use unique context: the thumbnail div follows overflow:`hidden`
patch(
    ':`relative`,overflow:`hidden`,minHeight:120},child',
    ':`relative`,overflow:`hidden`,minHeight:160},child',
    'thumbnail minHeight 120->160'
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
