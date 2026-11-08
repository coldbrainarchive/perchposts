#!/usr/bin/env python3
"""Patch v633 -> v634:
Make poster img pointerEvents:none so taps pass through to the video element.
Remove the no-op onClick. Video onClick already handles initial play.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v633.js'
dst = '_deploy/assets/index-DUcNPOLc-v634.js'

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
    ('src:_vpost,alt:' + q + q
     + ',style:{position:' + q + 'absolute' + q + ',inset:0,width:' + q + '100%' + q
     + ',height:' + q + '100%' + q + ',objectFit:' + q + 'cover' + q
     + ',borderRadius:10,cursor:' + q + 'pointer' + q + ',display:' + q + 'block' + q
     + '},onClick:_pe=>{return}}'),
    ('src:_vpost,alt:' + q + q
     + ',style:{position:' + q + 'absolute' + q + ',inset:0,width:' + q + '100%' + q
     + ',height:' + q + '100%' + q + ',objectFit:' + q + 'cover' + q
     + ',borderRadius:10,display:' + q + 'block' + q
     + ',pointerEvents:' + q + 'none' + q + '}}'),
    'poster img pointerEvents:none, remove onClick'
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
