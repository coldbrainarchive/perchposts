#!/usr/bin/env python3
"""Patch v650 -> v651:
Remove maxHeight manipulation from fullscreen enter/exit.
- requestFullscreen() overrides CSS anyway, so clearing maxHeight was unnecessary
- Clearing maxHeight was causing the video to stay large when _onFsExit fired late or missed
- Only swap objectFit (contain on enter, cover on exit) to fix the desktop crop issue
- maxHeight stays unchanged throughout, so layout always recovers correctly
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v650.js'
dst = '_deploy/assets/index-DUcNPOLc-v651.js'

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

# Remove maxHeight='' on fullscreen enter
patch(
    'v.style.objectFit=' + q + 'contain' + q + ';v.style.maxHeight=' + q + q + ';v.play();',
    'v.style.objectFit=' + q + 'contain' + q + ';v.play();',
    'remove maxHeight clear on fullscreen enter'
)

# Remove maxHeight restoration on fullscreen exit
patch(
    'v.style.opacity=' + q + q + ';v.style.objectFit=' + q + 'cover' + q + ';v.style.maxHeight=_mh+' + q + 'px' + q + ';v._exitingFs=!1;',
    'v.style.opacity=' + q + q + ';v.style.objectFit=' + q + 'cover' + q + ';v._exitingFs=!1;',
    'remove maxHeight restore on fullscreen exit'
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
