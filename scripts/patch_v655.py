#!/usr/bin/env python3
"""Patch v654 -> v655:
Remove all custom video UI (play bubble, poster overlay, fullscreen button,
custom onClick/onPlay/onPause handlers) and replace with native browser
controls. The entire position:relative container div + children are replaced
with a single <video controls> element.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v654.js'
dst = '_deploy/assets/index-DUcNPOLc-v655.js'

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

# Extract old string boundaries
old_start = ('(0,L.jsxs)(' + q + 'div' + q + ',{style:{position:' + q + 'relative' + q
             + ',marginTop:10},children:[(0,L.jsx)(' + q + 'video' + q
             + ',{src:n,controls:!1,playsInline:!0,loop:!0,preload:' + q + 'metadata' + q
             + ',style:{width:' + q + '100%' + q + ',maxHeight:_mh,objectFit:' + q + 'cover' + q
             + ',borderRadius:10,display:' + q + 'block' + q + ',cursor:' + q + 'pointer' + q + '},onClick:')
old_end = 'children:' + q + '⛶' + q + '})]})' # ⛶ char

# Build old by finding it
raw = open(src, encoding='utf-8').read()
si = raw.find(old_start)
ei = raw.find(old_end, si) + len(old_end)
old = raw[si:ei]

new = ('(0,L.jsx)(' + q + 'video' + q + ',{src:n,controls:!0,playsInline:!0,loop:!0,preload:' + q + 'metadata' + q
       + ',style:{width:' + q + '100%' + q + ',maxHeight:_mh,objectFit:' + q + 'cover' + q
       + ',borderRadius:10,display:' + q + 'block' + q + ',marginTop:10}})')

patch(old, new, 'replace custom UI with native controls video element')

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
