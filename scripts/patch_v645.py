#!/usr/bin/env python3
"""Patch v644 -> v645:
1. Increase default video maxH from 320 to 480
2. Increase fullscreen exit delay from 150ms to 400ms to give iOS more time
   to fully dismiss native controls before we reset the video state
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v644.js'
dst = '_deploy/assets/index-DUcNPOLc-v645.js'

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
    'function Fr({attachment:e,postId:o,maxH:_mh=320})',
    'function Fr({attachment:e,postId:o,maxH:_mh=480})',
    'increase default maxH to 480'
)

patch(
    'setTimeout(()=>{v.setAttribute(' + q + 'playsinline' + q + ',' + q + q + ');v.controls=!1;v.pause();},150)',
    'setTimeout(()=>{v.setAttribute(' + q + 'playsinline' + q + ',' + q + q + ');v.controls=!1;v.load();setTimeout(()=>{v.pause();},50);},400)',
    'increase fullscreen exit delay to 400ms + extra settle time before pause'
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
