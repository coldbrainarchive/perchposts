#!/usr/bin/env python3
"""Patch v680 -> v681:
Fix lightbox image sizing: portrait photos were being constrained by max-height:88vh
first, resulting in a width smaller than 92vw (black bars on sides). Change all three
lightboxes (postcard, comment, post detail) to use width:92vw so images always fill
the full viewport width regardless of aspect ratio.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v680.js'
dst = '_deploy/assets/index-DUcNPOLc-v681.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append('FAIL (' + label + '): not found')
    elif n > 3:
        errors.append('FAIL (' + label + '): ' + str(n) + ' matches (expected <=3)')
    else:
        content = content.replace(old, new)
        print('OK (' + str(n) + ' replacements): ' + label)

# Fix all three lightbox _im styles: force width:92vw so portrait photos fill the screen
patch(
    q + 'max-width:92vw;max-height:88vh;border-radius:10px;object-fit:contain;' + q,
    q + 'width:92vw;height:auto;max-height:88vh;border-radius:10px;' + q,
    'lightbox _im: width:92vw fills screen for all aspect ratios'
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
