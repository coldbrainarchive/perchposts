#!/usr/bin/env python3
"""Patch v698 -> v699:
Fix: chat-window uses flex-direction:column-reverse so scrollTop arithmetic is
inverted — our manual e.scrollTop=_n was wrong. Use t.scrollIntoView() instead,
which handles column-reverse and all ancestor scroll containers natively.
Also remove the now-redundant _cs.scrollIntoView since t.scrollIntoView covers it.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v698.js'
dst = '_deploy/assets/index-DUcNPOLc-v699.js'

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

# Replace the whole scroll+highlight block with t.scrollIntoView (handles column-reverse)
old_block = ('let _cs=document.querySelector(' + q + '.comments-shell' + q + ');'
             '_cs&&_cs.scrollIntoView({block:' + q + 'nearest' + q + '});'
             'let _n=Math.max(0,t.offsetTop-e.clientHeight/2+t.offsetHeight/2);'
             'e.scrollTop=_n;'
             'let _b=t.querySelector(' + q + '.chat-bubble' + q + ');'
             '_b&&(_b.classList.add(' + q + 'highlight' + q + '),'
             'setTimeout(()=>_b.classList.remove(' + q + 'highlight' + q + '),2500));'
             'setTimeout(()=>o(' + q + '/post/${r}' + q + ',{replace:!0}),1500)')

new_block = ('t.scrollIntoView({block:' + q + 'center' + q + ',behavior:' + q + 'instant' + q + '});'
             'let _b=t.querySelector(' + q + '.chat-bubble' + q + ');'
             '_b&&(_b.classList.add(' + q + 'highlight' + q + '),'
             'setTimeout(()=>_b.classList.remove(' + q + 'highlight' + q + '),2500));'
             'setTimeout(()=>o(' + q + '/post/${r}' + q + ',{replace:!0}),1500)')

patch(old_block, new_block, '[u,a]: use t.scrollIntoView to handle column-reverse correctly')

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
