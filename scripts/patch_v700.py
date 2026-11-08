#!/usr/bin/env python3
"""Patch v699 -> v700:
Replace single-fade highlight with 3 fast blinks using direct style manipulation.
Direct styles bypass the CSS transition so blinks are instant and always visible.
Pattern: 350ms on, 120ms off, 3 times.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v699.js'
dst = '_deploy/assets/index-DUcNPOLc-v700.js'

q = chr(0x60)
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

old_blink = ('t.scrollIntoView({block:' + q + 'center' + q + ',behavior:' + q + 'instant' + q + '});'
             'let _b=t.querySelector(' + q + '.chat-bubble' + q + ');'
             '_b&&(_b.classList.add(' + q + 'highlight' + q + '),'
             'setTimeout(()=>_b.classList.remove(' + q + 'highlight' + q + '),2500));'
             'setTimeout(()=>o(' + q + '/post/${r}' + q + ',{replace:!0}),1500)')

# Use requestAnimationFrame so layout is fully settled before scrollIntoView.
# Then 3 fast blinks (350ms on, 130ms off) via direct style (no CSS transition delay).
new_blink = ('requestAnimationFrame(()=>{'
             't.scrollIntoView({block:' + q + 'center' + q + ',behavior:' + q + 'instant' + q + '});'
             'let _b=t.querySelector(' + q + '.chat-bubble' + q + ');'
             'if(_b){let _bn=0;const _bl=()=>{'
             '_b.style.background=' + q + 'rgba(192,132,252,0.38)' + q + ';'
             '_b.style.outline=' + q + '2px solid rgba(192,132,252,0.75)' + q + ';'
             'setTimeout(()=>{'
             '_b.style.background=' + q + q + ';'
             '_b.style.outline=' + q + q + ';'
             '_bn++;if(_bn<3)setTimeout(_bl,130);'
             '},350);};_bl();}});'
             'setTimeout(()=>o(' + q + '/post/${r}' + q + ',{replace:!0}),1800)')

patch(old_blink, new_blink, 'highlight: 3 fast blinks via direct style (bypasses CSS transition)')

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
