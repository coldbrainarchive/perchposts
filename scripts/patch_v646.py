#!/usr/bin/env python3
"""Patch v645 -> v646:
1. Remove v.load() from fullscreen exit handler (was causing clunky X-button exit)
2. Use if(!v.paused)v.pause() so X-exit (already paused) is a no-op
3. Add _exitingFs flag: set before timeout, clear inside — so onPause suppresses
   the play bubble during the swipe-exit transition window
4. Reduce delay to 300ms (balanced between X and swipe)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v645.js'
dst = '_deploy/assets/index-DUcNPOLc-v646.js'

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

# Fix fullscreen exit: remove v.load(), add _exitingFs flag, use conditional pause
patch(
    'setTimeout(()=>{v.setAttribute(' + q + 'playsinline' + q + ',' + q + q + ');v.controls=!1;v.load();setTimeout(()=>{v.pause();},50);},400)',
    'v._exitingFs=!0;setTimeout(()=>{v._exitingFs=!1;v.setAttribute(' + q + 'playsinline' + q + ',' + q + q + ');v.controls=!1;if(!v.paused)v.pause();},300)',
    'remove v.load(), add _exitingFs flag, conditional pause, 300ms delay'
)

# Suppress play bubble in onPause when _exitingFs is true
patch(
    'onPause:e=>{const _vid=e.currentTarget;if(_vid._io){_vid._io.disconnect();_vid._io=null;}const pb=',
    'onPause:e=>{const _vid=e.currentTarget;if(_vid._io){_vid._io.disconnect();_vid._io=null;}if(_vid._exitingFs)return;const pb=',
    'suppress play bubble during fullscreen exit'
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
