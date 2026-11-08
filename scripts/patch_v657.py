#!/usr/bin/env python3
"""Patch v656 -> v657:
Re-add auto-pause on scroll via IntersectionObserver.
onPlay: start observer, disconnect existing one first.
onPause: disconnect observer.
No play bubble logic needed since we're using native controls.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v656.js'
dst = '_deploy/assets/index-DUcNPOLc-v657.js'

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
    ('src:n,controls:!0,playsInline:!0,loop:!0,preload:' + q + 'metadata' + q
     + ',poster:_vpost,style:'),
    ('src:n,controls:!0,playsInline:!0,loop:!0,preload:' + q + 'metadata' + q
     + ',poster:_vpost,'
     + 'onPlay:e=>{const _vp=e.currentTarget;if(_vp._io)_vp._io.disconnect();'
     + '_vp._io=new IntersectionObserver(([_en])=>{if(!_en.isIntersecting&&!_vp.paused)_vp.pause();},{threshold:0.2});'
     + '_vp._io.observe(_vp);},'
     + 'onPause:e=>{const _vid=e.currentTarget;if(_vid._io){_vid._io.disconnect();_vid._io=null;}},'
     + 'style:'),
    'add IntersectionObserver auto-pause on scroll'
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
