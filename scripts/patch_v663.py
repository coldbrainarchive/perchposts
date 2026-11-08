#!/usr/bin/env python3
"""Patch v662 -> v663:
Center attachments in the postcard on desktop by adding marginLeft/Right:auto.
Portrait content is narrower than the postcard, so centering distributes the
empty space equally on both sides rather than leaving a dead zone on the right.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v662.js'
dst = '_deploy/assets/index-DUcNPOLc-v663.js'

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

desktop = 'window.innerWidth>=768'

# Video element
patch(
    (',maxHeight:' + desktop + '?500:_mh'
     + ',borderRadius:10,display:' + q + 'block' + q + ',marginTop:10}'),
    (',maxHeight:' + desktop + '?500:_mh'
     + ',borderRadius:10,display:' + q + 'block' + q
     + ',marginTop:10,marginLeft:' + q + 'auto' + q + ',marginRight:' + q + 'auto' + q + '}'),
    'center video horizontally'
)

# Image element
patch(
    (',cursor:' + q + 'zoom-in' + q + '}'),
    (',cursor:' + q + 'zoom-in' + q
     + ',marginLeft:' + q + 'auto' + q + ',marginRight:' + q + 'auto' + q + '}'),
    'center image horizontally'
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
