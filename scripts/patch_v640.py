#!/usr/bin/env python3
"""Patch v639 -> v640:
Clean up UI when exiting fullscreen: restore playsinline attribute and pause
the video so the play bubble reappears and the inline view looks correct.
Listens for both fullscreenchange (desktop) and webkitendfullscreen (iOS).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v639.js'
dst = '_deploy/assets/index-DUcNPOLc-v640.js'

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
    ('v.removeAttribute(' + q + 'playsinline' + q + ');'
     + 'v.removeAttribute(' + q + 'webkit-playsinline' + q + ');'
     + 'v.play();'
     + 'if(v.requestFullscreen)v.requestFullscreen().catch(()=>{});'
     + 'else if(v.webkitEnterFullscreen)v.webkitEnterFullscreen();'),
    ('v.removeAttribute(' + q + 'playsinline' + q + ');'
     + 'v.removeAttribute(' + q + 'webkit-playsinline' + q + ');'
     + 'v.play();'
     + 'if(v.requestFullscreen)v.requestFullscreen().catch(()=>{});'
     + 'else if(v.webkitEnterFullscreen)v.webkitEnterFullscreen();'
     # Restore state on fullscreen exit
     + 'const _onFsExit=()=>{v.setAttribute(' + q + 'playsinline' + q + ',' + q + q + ');v.pause();};'
     + 'document.addEventListener(' + q + 'fullscreenchange' + q + ',()=>{if(!document.fullscreenElement)_onFsExit();},{once:!0});'
     + 'v.addEventListener(' + q + 'webkitendfullscreen' + q + ',_onFsExit,{once:!0});'),
    'restore playsinline + pause on fullscreen exit'
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
