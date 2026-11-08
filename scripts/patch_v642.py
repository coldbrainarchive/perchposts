#!/usr/bin/env python3
"""Patch v641 -> v642:
Fix overlapping UI on swipe-exit fullscreen on iOS.
Add 150ms delay + explicit v.controls=false so native controls clear
before our play bubble appears.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v641.js'
dst = '_deploy/assets/index-DUcNPOLc-v642.js'

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
    ('const _onFsExit=()=>{v.setAttribute(' + q + 'playsinline' + q + ',' + q + q + ');v.pause();};'
     + 'document.addEventListener(' + q + 'fullscreenchange' + q + ',()=>{if(!document.fullscreenElement)_onFsExit();},{once:!0});'
     + 'v.addEventListener(' + q + 'webkitendfullscreen' + q + ',_onFsExit,{once:!0});'),
    ('const _onFsExit=()=>{setTimeout(()=>{v.setAttribute(' + q + 'playsinline' + q + ',' + q + q + ');v.controls=!1;v.pause();},150);};'
     + 'document.addEventListener(' + q + 'fullscreenchange' + q + ',()=>{if(!document.fullscreenElement)_onFsExit();},{once:!0});'
     + 'v.addEventListener(' + q + 'webkitendfullscreen' + q + ',_onFsExit,{once:!0});'),
    'delay + clear controls on fullscreen exit'
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
