#!/usr/bin/env python3
"""Patch v632 -> v633:
Fix two-tap issue: iOS video elements capture touch even behind poster overlay.
Move initial-play logic into video onClick so one tap always works.
Also fix fullscreen: play first (loads video on iOS) then enter fullscreen.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v632.js'
dst = '_deploy/assets/index-DUcNPOLc-v633.js'

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

# 1. Video onClick: check if poster visible first (one-tap initial play)
new_video_click = (
    'onClick:e=>{const v=e.currentTarget;'
    + 'const poster=v.nextElementSibling;'
    + 'if(poster&&poster.tagName===' + q + 'IMG' + q + '&&poster.style.display!==' + q + 'none' + q + '){'
    + 'poster.style.display=' + q + 'none' + q + ';'
    + 'const pb=poster.nextElementSibling;if(pb)pb.style.display=' + q + 'none' + q + ';'
    + 'v.controls=!1;v.play();'
    + '}else{if(v.paused){v.play();}else{v.pause();}}}'
)
patch(
    'onClick:e=>{const v=e.currentTarget;if(v.paused){v.play();}else{v.pause();}}',
    new_video_click,
    'video onClick handles initial play in one tap'
)

# 2. Remove poster onClick (video onClick now handles it)
patch(
    '_pe.currentTarget.style.display=' + q + 'none' + q
    + ';_pe.currentTarget.nextElementSibling.style.display=' + q + 'none' + q
    + ';const _pv=_pe.currentTarget.previousElementSibling;_pv.controls=!1;_pv.play()}}',
    'return}}',
    'poster onClick now no-op (video onClick handles initial play)'
)

# 3. Fix fullscreen button: play first to ensure loaded, then enter fullscreen
old_fs = (
    'if(v.webkitEnterFullscreen){v.webkitEnterFullscreen();}'
    + 'else if(v.requestFullscreen){'
    + 'v.controls=!0;v.requestFullscreen();'
    + 'document.addEventListener(' + q + 'fullscreenchange' + q + ',()=>{if(!document.fullscreenElement)v.controls=!1;},{once:!0});}'
)
new_fs = (
    'const _doFs=()=>{if(v.webkitEnterFullscreen){v.webkitEnterFullscreen();}'
    + 'else if(v.requestFullscreen){v.controls=!0;v.requestFullscreen();'
    + 'document.addEventListener(' + q + 'fullscreenchange' + q + ',()=>{if(!document.fullscreenElement)v.controls=!1;},{once:!0});}};'
    + 'if(v.readyState<1){v.load();v.addEventListener(' + q + 'loadedmetadata' + q + ',_doFs,{once:!0});}else{_doFs();}'
)
patch(old_fs, new_fs, 'fullscreen loads metadata first if needed')

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
