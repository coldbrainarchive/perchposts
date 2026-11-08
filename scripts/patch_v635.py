#!/usr/bin/env python3
"""Patch v634 -> v635:
Fix 1: onPause captures video ref before e.currentTarget goes null after handler returns.
Fix 2: Simpler fullscreen — try both APIs, no async dance.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v634.js'
dst = '_deploy/assets/index-DUcNPOLc-v635.js'

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

# Fix 1: capture video ref before handler exits so closure works
patch(
    ('onPause:e=>{const pb=e.currentTarget.nextElementSibling&&e.currentTarget.nextElementSibling.nextElementSibling;'
     + 'if(pb){pb.style.display=' + q + 'flex' + q + ';pb.style.pointerEvents=' + q + 'auto' + q + ';'
     + 'pb.onclick=()=>{pb.style.display=' + q + 'none' + q + ';pb.style.pointerEvents=' + q + 'none' + q + ';e.currentTarget.play();}}}'),
    ('onPause:e=>{const _vid=e.currentTarget;'
     + 'const pb=_vid.nextElementSibling&&_vid.nextElementSibling.nextElementSibling;'
     + 'if(pb){pb.style.display=' + q + 'flex' + q + ';pb.style.pointerEvents=' + q + 'auto' + q + ';'
     + 'pb.onclick=()=>{pb.style.display=' + q + 'none' + q + ';pb.style.pointerEvents=' + q + 'none' + q + ';_vid.play();}}}'),
    'capture video ref in onPause before currentTarget goes null'
)

# Fix 2: simpler fullscreen — try webkitEnterFullscreen first, then requestFullscreen
patch(
    ('const _doFs=()=>{if(v.webkitEnterFullscreen){v.webkitEnterFullscreen();}'
     + 'else if(v.requestFullscreen){v.controls=!0;v.requestFullscreen();'
     + 'document.addEventListener(' + q + 'fullscreenchange' + q + ',()=>{if(!document.fullscreenElement)v.controls=!1;},{once:!0});}};'
     + 'if(v.readyState<1){v.load();v.addEventListener(' + q + 'loadedmetadata' + q + ',_doFs,{once:!0});}else{_doFs();}'),
    ('try{if(v.webkitEnterFullscreen){v.webkitEnterFullscreen();}'
     + 'else if(v.requestFullscreen){v.requestFullscreen();}}catch(_e){}'),
    'simplify fullscreen call'
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
