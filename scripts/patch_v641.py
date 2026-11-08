#!/usr/bin/env python3
"""Patch v640 -> v641: Add loop:!0 to video element so videos loop automatically."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v640.js'
dst = '_deploy/assets/index-DUcNPOLc-v641.js'

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
    'src:n,controls:!1,playsInline:!0,preload:' + q + 'metadata' + q,
    'src:n,controls:!1,playsInline:!0,loop:!0,preload:' + q + 'metadata' + q,
    'add loop to video'
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
