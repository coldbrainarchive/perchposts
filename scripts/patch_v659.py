#!/usr/bin/env python3
"""Patch v657 -> v659:
Native controls with auto-hide after 900ms:
- onPlay: start 900ms timer, then controls=false
- onClick: show controls, reset 900ms timer
- onPause: clear timer, controls=true (so scrubber/play visible while paused)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v657.js'
dst = '_deploy/assets/index-DUcNPOLc-v659.js'

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

# 1. onPlay: add auto-hide timer after IntersectionObserver setup
patch(
    '_vp._io.observe(_vp);},onPause:',
    '_vp._io.observe(_vp);if(_vp._ct)clearTimeout(_vp._ct);_vp._ct=setTimeout(()=>{_vp.controls=!1;},900);},onPause:',
    'auto-hide controls 900ms after play'
)

# 2. onPause: clear timer, restore controls so scrubber is visible while paused
patch(
    'onPause:e=>{const _vid=e.currentTarget;if(_vid._io){_vid._io.disconnect();_vid._io=null;}},',
    'onPause:e=>{const _vid=e.currentTarget;if(_vid._io){_vid._io.disconnect();_vid._io=null;}if(_vid._ct)clearTimeout(_vid._ct);_vid.controls=!0;},',
    'show controls on pause, clear hide timer'
)

# 3. Add onClick: tap while playing shows controls and resets the hide timer
patch(
    'poster:_vpost,onPlay:',
    'poster:_vpost,onClick:e=>{const _v=e.currentTarget;_v.controls=!0;if(_v._ct)clearTimeout(_v._ct);_v._ct=setTimeout(()=>{_v.controls=!1;},900);},onPlay:',
    'tap while playing shows controls for 900ms'
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
