#!/usr/bin/env python3
"""Patch v637 -> v638:
iOS fullscreen fix: remove playsinline attribute before play() so iOS
automatically enters fullscreen (without playsinline, iOS goes fullscreen on play).
Desktop: still uses requestFullscreen().
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v637.js'
dst = '_deploy/assets/index-DUcNPOLc-v638.js'

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
    'if(v.webkitEnterFullscreen){v.play();v.webkitEnterFullscreen();}else if(v.requestFullscreen){v.play();v.requestFullscreen().catch(()=>{});}',
    ('v.removeAttribute(' + q + 'playsinline' + q + ');'
     + 'v.removeAttribute(' + q + 'webkit-playsinline' + q + ');'
     + 'v.play();'
     + 'if(!v.webkitEnterFullscreen&&v.requestFullscreen)v.requestFullscreen().catch(()=>{});'),
    'remove playsinline before play so iOS auto-fullscreens'
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
