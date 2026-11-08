#!/usr/bin/env python3
"""Patch v631 -> v632:
Fix: restore pointerEvents:none on play bubble outer div in JSX.
Without it the bubble (position:absolute;inset:0) sits on top of the poster
and eats every tap. The onPause handler still sets pointerEvents:auto dynamically.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v631.js'
dst = '_deploy/assets/index-DUcNPOLc-v632.js'

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

# Restore pointerEvents:none on play bubble outer div
patch(
    'ition:' + q + 'absolute' + q + ',inset:0,display:' + q + 'flex' + q + ',alignItems:' + q + 'center' + q + ',justifyContent:' + q + 'center' + q + ',borderRadius:10}',
    'ition:' + q + 'absolute' + q + ',inset:0,display:' + q + 'flex' + q + ',alignItems:' + q + 'center' + q + ',justifyContent:' + q + 'center' + q + ',pointerEvents:' + q + 'none' + q + ',borderRadius:10}',
    'restore pointerEvents:none on play bubble'
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
