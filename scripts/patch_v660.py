#!/usr/bin/env python3
"""Patch v657 -> v660:
On desktop (window.innerWidth >= 768), remove maxHeight cap and switch
objectFit to contain so attachments show at their actual size without cropping.
Mobile keeps maxHeight:_mh + objectFit:cover as before.
Patches both the image element and the video element in Fr.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v657.js'
dst = '_deploy/assets/index-DUcNPOLc-v660.js'

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

# Image element (has cursor:zoom-in as unique context)
patch(
    ('style:{width:' + q + '100%' + q + ',borderRadius:10,display:' + q + 'block' + q
     + ',maxHeight:_mh,objectFit:' + q + 'cover' + q + ',cursor:' + q + 'zoom-in' + q + '}'),
    ('style:{width:' + q + '100%' + q + ',borderRadius:10,display:' + q + 'block' + q
     + ',maxHeight:' + desktop + '?void 0:_mh'
     + ',objectFit:' + desktop + '?' + q + 'contain' + q + ':' + q + 'cover' + q
     + ',cursor:' + q + 'zoom-in' + q + '}'),
    'image: desktop actual size'
)

# Video element (has marginTop:10 as unique context)
patch(
    ('style:{width:' + q + '100%' + q + ',maxHeight:_mh,objectFit:' + q + 'cover' + q
     + ',borderRadius:10,display:' + q + 'block' + q + ',marginTop:10}'),
    ('style:{width:' + q + '100%' + q
     + ',maxHeight:' + desktop + '?void 0:_mh'
     + ',objectFit:' + desktop + '?' + q + 'contain' + q + ':' + q + 'cover' + q
     + ',borderRadius:10,display:' + q + 'block' + q + ',marginTop:10}'),
    'video: desktop actual size'
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
