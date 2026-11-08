#!/usr/bin/env python3
"""Patch v660 -> v661:
Replace void 0 (uncapped) with 500px for desktop maxHeight.
Shows full attachment without cropping (objectFit:contain) but keeps
a reasonable size so it doesn't fill the screen.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v660.js'
dst = '_deploy/assets/index-DUcNPOLc-v661.js'

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

# Both image and video have the same maxHeight ternary - replace void 0 with 500
patch(
    'maxHeight:window.innerWidth>=768?void 0:_mh,objectFit:window.innerWidth>=768?`contain`:`cover`,borderRadius:10,display:`block`,marginTop:10}',
    'maxHeight:window.innerWidth>=768?500:_mh,objectFit:window.innerWidth>=768?`contain`:`cover`,borderRadius:10,display:`block`,marginTop:10}',
    'video: desktop maxHeight 500px'
)

patch(
    'maxHeight:window.innerWidth>=768?void 0:_mh,objectFit:window.innerWidth>=768?`contain`:`cover`,cursor:`zoom-in`}',
    'maxHeight:window.innerWidth>=768?500:_mh,objectFit:window.innerWidth>=768?`contain`:`cover`,cursor:`zoom-in`}',
    'image: desktop maxHeight 500px'
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
