#!/usr/bin/env python3
"""Patch v690 -> v691:
Desktop only: make multi-photo stacked card thumbnails match the single-photo Fr
component — use height:auto + maxHeight:480 instead of fixed height, so images
show at natural proportions. Badge stays at top:8,right:8 of the container.
Mobile unchanged (keeps fixed height + cover crop).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v690.js'
dst = '_deploy/assets/index-DUcNPOLc-v691.js'

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

tail_10 = (',objectFit:window.innerWidth>=768?' + q + 'contain' + q + ':' + q + 'cover' + q
           + ',borderRadius:10,display:' + q + 'block' + q + ',cursor:' + q + 'zoom-in' + q
           + ',position:' + q + 'relative' + q + ',zIndex:1')
tail_8  = (',objectFit:window.innerWidth>=768?' + q + 'contain' + q + ':' + q + 'cover' + q
           + ',borderRadius:8,display:' + q + 'block' + q + ',cursor:' + q + 'zoom-in' + q
           + ',position:' + q + 'relative' + q + ',zIndex:1')

base = 'width:' + q + '100%' + q + ',height:'

# h:320 (postcard + post-detail): desktop gets auto height + maxHeight:480
patch_all(
    base + '320' + tail_10,
    (base + '(window.innerWidth>=768?' + q + 'auto' + q + ':320)'
     + ',maxHeight:window.innerWidth>=768?480:void 0'
     + tail_10),
    'stacked h:320 -> auto+maxHeight on desktop'
)

# h:240 (comment): same
patch_all(
    base + '240' + tail_8,
    (base + '(window.innerWidth>=768?' + q + 'auto' + q + ':240)'
     + ',maxHeight:window.innerWidth>=768?480:void 0'
     + tail_8),
    'stacked h:240 -> auto+maxHeight on desktop'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

src_content = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (src_content.count('(') - src_content.count(')'))
b_delta = (content.count('{') - content.count('}')) - (src_content.count('{') - src_content.count('}'))
print('Paren delta: ' + str(p_delta) + ', Brace delta: ' + str(b_delta))
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
