#!/usr/bin/env python3
"""Patch v626 -> v627:
Remove native controls toggle on pause — just play/pause silently.
No native control bar ever appears (no glitchy white play/skip/seek overlay).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v626.js'
dst = '_deploy/assets/index-DUcNPOLc-v627.js'

content = open(src, encoding='utf-8').read()
errors = []

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
    'onClick:e=>{const v=e.currentTarget;if(v.paused){v.controls=!1;v.play();}else{v.pause();v.controls=!0;}}',
    'onClick:e=>{const v=e.currentTarget;if(v.paused){v.play();}else{v.pause();}}',
    'remove native controls toggle — silent play/pause'
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
