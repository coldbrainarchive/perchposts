#!/usr/bin/env python3
"""Patch v683 -> v684:
Preload remaining photos earlier: add onLoad to each stacked card thumbnail image
so photos 2-N start fetching as soon as photo 1 renders in the feed, long before
the user taps to open the lightbox.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v683.js'
dst = '_deploy/assets/index-DUcNPOLc-v684.js'

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

# Add onLoad preload right after src= for each stacked card thumbnail
for var, h in [('_pAtts', '320'), ('_cAtts', '240'), ('_tAtts', '320')]:
    old = ('{src:' + var + '[0].url,style:{width:' + q + '100%' + q + ',height:' + h)
    new = ('{src:' + var + '[0].url'
           + ',onLoad:()=>{' + var + '.slice(1).forEach(_a=>{new Image().src=_a.url;})}'
           + ',style:{width:' + q + '100%' + q + ',height:' + h)
    patch(old, new, f'{var}: preload photos 2+ on thumbnail load')

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
