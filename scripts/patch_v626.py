#!/usr/bin/env python3
"""Patch v624 -> v626:
Video playback UX:
- No native controls shown by default (controls:!1)
- Tap poster: plays video, hides poster/play-button overlay (no controls bar)
- Tap video while playing: pauses and shows controls so user can seek
- Tap video while paused: resumes and hides controls
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v624.js'
dst = '_deploy/assets/index-DUcNPOLc-v626.js'

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

# 1. Video element: remove controls, add tap-to-pause onClick
patch(
    '(0,L.jsx)(' + q + 'video' + q + ',{src:n,controls:!0,playsInline:!0,preload:' + q + 'metadata' + q + ',style:{maxWidth:' + q + '100%' + q + ',borderRadius:10,maxHeight:_mh,display:' + q + 'block' + q + '}})',
    '(0,L.jsx)(' + q + 'video' + q + ',{src:n,controls:!1,playsInline:!0,preload:' + q + 'metadata' + q + ',style:{maxWidth:' + q + '100%' + q + ',borderRadius:10,maxHeight:_mh,display:' + q + 'block' + q + ',cursor:' + q + 'pointer' + q + '},onClick:e=>{const v=e.currentTarget;if(v.paused){v.controls=!1;v.play();}else{v.pause();v.controls=!0;}}})',
    'video tap-to-pause, show controls only when paused'
)

# 2. Poster onClick: play with controls hidden
patch(
    '_pe.currentTarget.nextElementSibling.style.display=' + q + 'none' + q + ';_pe.currentTarget.previousElementSibling.play()}})',
    '_pe.currentTarget.nextElementSibling.style.display=' + q + 'none' + q + ';const _pv=_pe.currentTarget.previousElementSibling;_pv.controls=!1;_pv.play()}})',
    'poster onClick plays with controls hidden'
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
