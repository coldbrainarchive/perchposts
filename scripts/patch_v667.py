#!/usr/bin/env python3
"""Patch v666 -> v667:
Mobile only: after exiting iOS native fullscreen (webkitendfullscreen),
resume playback in the inline preview after a short settle delay.
Guard with _fsResume flag to avoid duplicate listeners.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v666.js'
dst = '_deploy/assets/index-DUcNPOLc-v667.js'

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
    '_vp.addEventListener(' + q + 'fullscreenchange' + q + ',_vp._fsOf);}}',
    ('_vp.addEventListener(' + q + 'fullscreenchange' + q + ',_vp._fsOf);}'
     + 'if(window.innerWidth<768&&!_vp._fsResume){'
     + '_vp._fsResume=()=>{setTimeout(()=>{if(_vp.paused)_vp.play();},150);};'
     + '_vp.addEventListener(' + q + 'webkitendfullscreen' + q + ',_vp._fsResume);}}'
    ),
    'mobile: resume playback after webkitendfullscreen'
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
