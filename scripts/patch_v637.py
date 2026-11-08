#!/usr/bin/env python3
"""Patch v636 -> v637:
Fix fullscreen on mobile iOS: webkitEnterFullscreen() requires the video to be
playing AND must be called synchronously in the same user gesture.
Call v.play() then v.webkitEnterFullscreen() together in the onclick handler.
Also hide poster/play-bubble so the video is ready to show.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v636.js'
dst = '_deploy/assets/index-DUcNPOLc-v637.js'

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
    ('if(v.requestFullscreen){'
     + 'v.requestFullscreen().catch(()=>{if(v.webkitEnterFullscreen)v.webkitEnterFullscreen();});'
     + '}else if(v.webkitEnterFullscreen){v.webkitEnterFullscreen();}'),
    ('const poster=v.nextElementSibling;'
     + 'if(poster&&poster.tagName===' + q + 'IMG' + q + ')poster.style.display=' + q + 'none' + q + ';'
     + 'const pb=poster&&poster.nextElementSibling;'
     + 'if(pb)pb.style.display=' + q + 'none' + q + ';'
     + 'if(v.webkitEnterFullscreen){'
     + 'v.play();v.webkitEnterFullscreen();'
     + '}else if(v.requestFullscreen){'
     + 'v.play();v.requestFullscreen().catch(()=>{});}'),
    'iOS fullscreen: play+webkitEnterFullscreen synchronously in user gesture'
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
