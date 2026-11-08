#!/usr/bin/env python3
"""Patch v688 -> v689:
Fix desktop video cropping:
1. Use objectFit:contain on desktop so portrait videos are never cropped in normal view
2. Fix fullscreen handler to listen on document (not element) and add webkitfullscreenchange
   so Chrome fullscreen always shows the full video without cropping
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v688.js'
dst = '_deploy/assets/index-DUcNPOLc-v689.js'

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

# 1. Video style: objectFit:cover -> contain on desktop, cover on mobile
patch(
    'objectFit:' + q + 'cover' + q + ',borderRadius:10,display:' + q + 'block' + q + ',marginTop:10',
    'objectFit:window.innerWidth>=768?' + q + 'contain' + q + ':' + q + 'cover' + q + ',borderRadius:10,display:' + q + 'block' + q + ',marginTop:10',
    'video objectFit: contain on desktop, cover on mobile'
)

# 2. Fullscreen handler: listen on document instead of element, add webkit event,
#    always set contain (no toggling needed since desktop default is now contain)
patch(
    '_vp._fsOf=()=>{_vp.style.objectFit=(document.fullscreenElement||document.webkitFullscreenElement)?'
    + q + 'contain' + q + ':' + q + 'cover' + q
    + ';};_vp.addEventListener(' + q + 'fullscreenchange' + q + ',_vp._fsOf);}',
    '_vp._fsOf=()=>{_vp.style.objectFit=' + q + 'contain' + q + '};'
    + 'document.addEventListener(' + q + 'fullscreenchange' + q + ',_vp._fsOf);'
    + 'document.addEventListener(' + q + 'webkitfullscreenchange' + q + ',_vp._fsOf);}',
    'fullscreen handler: document listener + webkit + always contain'
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
