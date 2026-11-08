#!/usr/bin/env python3
"""Patch v642 -> v643:
Auto-pause video when it scrolls off screen using IntersectionObserver.
Observer starts on play, disconnects on pause.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v642.js'
dst = '_deploy/assets/index-DUcNPOLc-v643.js'

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

# Extend onPlay to set up IntersectionObserver
patch(
    ('onPlay:e=>{const pb=e.currentTarget.nextElementSibling&&e.currentTarget.nextElementSibling.nextElementSibling;'
     + 'if(pb)pb.style.display=' + q + 'none' + q + '}'),
    ('onPlay:e=>{const pb=e.currentTarget.nextElementSibling&&e.currentTarget.nextElementSibling.nextElementSibling;'
     + 'if(pb)pb.style.display=' + q + 'none' + q + ';'
     + 'const _vp=e.currentTarget;'
     + 'if(_vp._io)_vp._io.disconnect();'
     + '_vp._io=new IntersectionObserver(([_en])=>{if(!_en.isIntersecting&&!_vp.paused)_vp.pause();},{threshold:0.2});'
     + '_vp._io.observe(_vp);}'),
    'onPlay sets up IntersectionObserver to pause when off screen'
)

# Extend onPause to disconnect observer
patch(
    ('onPause:e=>{const _vid=e.currentTarget;'
     + 'const pb=_vid.nextElementSibling&&_vid.nextElementSibling.nextElementSibling;'),
    ('onPause:e=>{const _vid=e.currentTarget;'
     + 'if(_vid._io){_vid._io.disconnect();_vid._io=null;}'
     + 'const pb=_vid.nextElementSibling&&_vid.nextElementSibling.nextElementSibling;'),
    'onPause disconnects IntersectionObserver'
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
