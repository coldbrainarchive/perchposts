#!/usr/bin/env python3
"""Patch v678 -> v679: Fix comment shadows that were missed in v678."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v678.js'
dst = '_deploy/assets/index-DUcNPOLc-v679.js'

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

patch(
    'top:-10,left:-10,right:0,bottom:0,borderRadius:8,background:' + q + '#252836' + q + ',zIndex:0}',
    'top:-13,left:-13,right:0,bottom:0,borderRadius:8,background:' + q + '#3a3d4e' + q + ',zIndex:0,transform:' + q + 'rotate(-5deg)' + q + '}',
    'comment shadow 2: rotate + brighter'
)
patch(
    'top:-5,left:-5,right:0,bottom:0,borderRadius:8,background:' + q + '#1e2130' + q + ',zIndex:0}',
    'top:-7,left:-7,right:0,bottom:0,borderRadius:8,background:' + q + '#2e3140' + q + ',zIndex:0,transform:' + q + 'rotate(-2.5deg)' + q + '}',
    'comment shadow 1: rotate + brighter'
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
