#!/usr/bin/env python3
"""Patch v657 -> v658:
Two-tap video UX:
- controls:false by default (no control bar on load)
- Tap 1 (paused): plays the video, controls stay hidden
- Tap 2 (playing): reveals native controls (timeline, fullscreen, etc.)
- onPause: resets controls=false so next play cycle starts clean again
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v657.js'
dst = '_deploy/assets/index-DUcNPOLc-v658.js'

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

# 1. Disable native controls by default
patch(
    'src:n,controls:!0,playsInline:!0',
    'src:n,controls:!1,playsInline:!0',
    'controls:false by default'
)

# 2. Add onClick: tap1=play, tap2=reveal controls
patch(
    'poster:_vpost,onPlay:e=>{const _vp=e.currentTarget;',
    ('poster:_vpost,'
     + 'onClick:e=>{const v=e.currentTarget;if(v.paused){v.play();}else{v.controls=!0;}},onPlay:e=>{const _vp=e.currentTarget;'),
    'tap1=play tap2=show controls onClick handler'
)

# 3. Reset controls=false on pause so next play cycle starts clean
patch(
    'onPause:e=>{const _vid=e.currentTarget;if(_vid._io){_vid._io.disconnect();_vid._io=null;}},',
    'onPause:e=>{const _vid=e.currentTarget;if(_vid._io){_vid._io.disconnect();_vid._io=null;}_vid.controls=!1;},',
    'reset controls=false on pause'
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
