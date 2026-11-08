#!/usr/bin/env python3
"""Patch v689 -> v690:
Apply objectFit:contain on desktop for all photo displays, matching the video fix:
- Fr single photo: contain on desktop, cover on mobile
- Stacked card thumbnails (postcard h:320, comment h:240, post-detail h:320): same
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v689.js'
dst = '_deploy/assets/index-DUcNPOLc-v690.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch_all(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append('FAIL (' + label + '): not found')
    else:
        content = content.replace(old, new)
        print(f'OK ({n}x): ' + label)

# Fr single photo: objectFit:cover,cursor:zoom-in -> conditional
patch_all(
    'objectFit:' + q + 'cover' + q + ',cursor:' + q + 'zoom-in' + q,
    'objectFit:window.innerWidth>=768?' + q + 'contain' + q + ':' + q + 'cover' + q + ',cursor:' + q + 'zoom-in' + q,
    'Fr image: contain on desktop'
)

# Stacked card h:320 (postcard + post detail): cover -> conditional
patch_all(
    'width:' + q + '100%' + q + ',height:320,objectFit:' + q + 'cover' + q + ',borderRadius:10,display:' + q + 'block' + q + ',cursor:' + q + 'zoom-in' + q,
    'width:' + q + '100%' + q + ',height:320,objectFit:window.innerWidth>=768?' + q + 'contain' + q + ':' + q + 'cover' + q + ',borderRadius:10,display:' + q + 'block' + q + ',cursor:' + q + 'zoom-in' + q,
    'stacked h:320: contain on desktop'
)

# Stacked card h:240 (comment): cover -> conditional
patch_all(
    'width:' + q + '100%' + q + ',height:240,objectFit:' + q + 'cover' + q + ',borderRadius:8,display:' + q + 'block' + q + ',cursor:' + q + 'zoom-in' + q,
    'width:' + q + '100%' + q + ',height:240,objectFit:window.innerWidth>=768?' + q + 'contain' + q + ':' + q + 'cover' + q + ',borderRadius:8,display:' + q + 'block' + q + ',cursor:' + q + 'zoom-in' + q,
    'stacked h:240: contain on desktop'
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
