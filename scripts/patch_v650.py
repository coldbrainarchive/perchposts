#!/usr/bin/env python3
"""Patch v649 -> v650:
1. On fullscreen enter: switch video to objectFit:contain + no maxHeight so
   desktop fullscreen shows the whole video without cropping.
2. On fullscreen exit: restore objectFit:cover + maxHeight inside the timeout,
   and extend timeout to 500ms to cover slower iOS transition animations.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v649.js'
dst = '_deploy/assets/index-DUcNPOLc-v650.js'

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

# On fullscreen enter: switch to contain so desktop doesn't crop
patch(
    ('v.removeAttribute(' + q + 'playsinline' + q + ');v.removeAttribute(' + q + 'webkit-playsinline' + q + ');v.play();'),
    ('v.removeAttribute(' + q + 'playsinline' + q + ');v.removeAttribute(' + q + 'webkit-playsinline' + q + ');'
     + 'v.style.objectFit=' + q + 'contain' + q + ';v.style.maxHeight=' + q + q + ';v.play();'),
    'objectFit:contain + no maxHeight on fullscreen enter'
)

# On fullscreen exit: restore objectFit:cover + maxHeight, extend to 500ms
patch(
    ('v.style.opacity=' + q + q + ';v._exitingFs=!1;if(!v.paused)v.pause();'
     + 'const _pb=v.nextElementSibling&&v.nextElementSibling.nextElementSibling;'
     + 'if(_pb&&v.paused){_pb.style.display=' + q + 'flex' + q + ';_pb.style.pointerEvents=' + q + 'auto' + q + ';'
     + '_pb.onclick=()=>{_pb.style.display=' + q + 'none' + q + ';_pb.style.pointerEvents=' + q + 'none' + q + ';v.play();};}},300)'),
    ('v.style.opacity=' + q + q + ';v.style.objectFit=' + q + 'cover' + q + ';v.style.maxHeight=_mh+' + q + 'px' + q + ';'
     + 'v._exitingFs=!1;if(!v.paused)v.pause();'
     + 'const _pb=v.nextElementSibling&&v.nextElementSibling.nextElementSibling;'
     + 'if(_pb&&v.paused){_pb.style.display=' + q + 'flex' + q + ';_pb.style.pointerEvents=' + q + 'auto' + q + ';'
     + '_pb.onclick=()=>{_pb.style.display=' + q + 'none' + q + ';_pb.style.pointerEvents=' + q + 'none' + q + ';v.play();};}},500)'),
    'restore objectFit:cover + maxHeight on exit, extend timeout to 500ms'
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
