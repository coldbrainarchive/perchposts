#!/usr/bin/env python3
"""Patch v635 -> v636:
Fix fullscreen: try requestFullscreen() first (iOS 16.4+ standard),
catch/fallback to webkitEnterFullscreen() for older iOS.
requestFullscreen returns a Promise so handle rejection properly.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v635.js'
dst = '_deploy/assets/index-DUcNPOLc-v636.js'

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
    'try{if(v.webkitEnterFullscreen){v.webkitEnterFullscreen();}else if(v.requestFullscreen){v.requestFullscreen();}}catch(_e){}',
    ('if(v.requestFullscreen){'
     + 'v.requestFullscreen().catch(()=>{if(v.webkitEnterFullscreen)v.webkitEnterFullscreen();});'
     + '}else if(v.webkitEnterFullscreen){v.webkitEnterFullscreen();}'),
    'requestFullscreen first with catch fallback to webkitEnterFullscreen'
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
