#!/usr/bin/env python3
"""Patch v685 -> v686:
Make single photo and video fill the full post width on desktop, just like the
multi-photo stacked card. Previously Fr used width:'auto' on desktop (>=768px)
which sized to natural dimensions, leaving empty space. Change to width:'100%'.
Also remove the desktop-specific 'contain' objectFit for images (use 'cover' to fill).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v685.js'
dst = '_deploy/assets/index-DUcNPOLc-v686.js'

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

# Image in Fr: width:auto on desktop -> width:100%, objectFit contain -> cover
patch(
    ('width:window.innerWidth>=768?' + q + 'auto' + q + ':' + q + '100%' + q + ','
     'maxWidth:' + q + '100%' + q + ',borderRadius:10,display:' + q + 'block' + q + ','
     'maxHeight:window.innerWidth>=768?500:_mh,'
     'objectFit:window.innerWidth>=768?' + q + 'contain' + q + ':' + q + 'cover' + q + ','
     'cursor:' + q + 'zoom-in' + q),
    ('width:' + q + '100%' + q + ','
     'maxWidth:' + q + '100%' + q + ',borderRadius:10,display:' + q + 'block' + q + ','
     'maxHeight:_mh,'
     'objectFit:' + q + 'cover' + q + ','
     'cursor:' + q + 'zoom-in' + q),
    'Fr image: fill full post width'
)

# Video in Fr: width:auto on desktop -> width:100%
patch(
    ('width:window.innerWidth>=768?' + q + 'auto' + q + ':' + q + '100%' + q + ','
     'maxWidth:' + q + '100%' + q + ','
     'maxHeight:window.innerWidth>=768?500:_mh,'
     'objectFit:' + q + 'cover' + q + ',borderRadius:10,display:' + q + 'block' + q + ',marginTop:10'),
    ('width:' + q + '100%' + q + ','
     'maxHeight:_mh,'
     'objectFit:' + q + 'cover' + q + ',borderRadius:10,display:' + q + 'block' + q + ',marginTop:10'),
    'Fr video: fill full post width'
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
