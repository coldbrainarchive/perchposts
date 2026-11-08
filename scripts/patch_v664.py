#!/usr/bin/env python3
"""Patch v661 -> v664:
Fix black sidebars on desktop video only. Do not touch mobile or images.
Desktop video: width:auto + maxWidth:100% so portrait video renders at
natural width with no letterboxing. Mobile keeps width:100% + objectFit:cover.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v661.js'
dst = '_deploy/assets/index-DUcNPOLc-v664.js'

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

# Video only (unique context: marginTop:10)
patch(
    ('style:{width:' + q + '100%' + q
     + ',maxHeight:' + desktop + '?500:_mh'
     + ',objectFit:' + desktop + '?' + q + 'contain' + q + ':' + q + 'cover' + q
     + ',borderRadius:10,display:' + q + 'block' + q + ',marginTop:10}'),
    ('style:{width:' + desktop + '?' + q + 'auto' + q + ':' + q + '100%' + q
     + ',maxWidth:' + q + '100%' + q
     + ',maxHeight:' + desktop + '?500:_mh'
     + ',objectFit:' + q + 'cover' + q
     + ',borderRadius:10,display:' + q + 'block' + q + ',marginTop:10}'),
    'video desktop: width:auto (no black bars), mobile unchanged'
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
