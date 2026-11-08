#!/usr/bin/env python3
"""Patch v655 -> v656:
Add poster:_vpost to the native video element so the thumbnail shows
before the video plays. _vpost is already destructured from the attachment.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v655.js'
dst = '_deploy/assets/index-DUcNPOLc-v656.js'

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

patch(
    'src:n,controls:!0,playsInline:!0,loop:!0,preload:' + q + 'metadata' + q + ',style:',
    'src:n,controls:!0,playsInline:!0,loop:!0,preload:' + q + 'metadata' + q + ',poster:_vpost,style:',
    'add poster:_vpost to video element'
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
