#!/usr/bin/env python3
"""Patch v686 -> v687:
Fix desktop lightbox to show images at real/natural dimensions:
- Desktop (>=768px): max-width:92vw (image shows at natural size, constrained only if too large)
- Mobile (<768px): width:92vw (forces portrait photos to fill screen width)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v686.js'
dst = '_deploy/assets/index-DUcNPOLc-v687.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

old_im = (q + 'width:92vw;height:auto;max-height:${Math.round(_ih*0.88)}px;'
          'border-radius:10px;transition:opacity 0.2s;' + q)

new_im = (q + "${window.innerWidth>=768?'max-width':'width'}:92vw;height:auto;"
          'max-height:${Math.round(_ih*0.88)}px;'
          'border-radius:10px;transition:opacity 0.2s;' + q)

n = content.count(old_im)
if n == 0:
    errors.append('FAIL (_im style): not found')
elif n > 3:
    errors.append('FAIL (_im style): ' + str(n) + ' matches')
else:
    content = content.replace(old_im, new_im)
    print(f'OK ({n} replacements): lightbox _im: max-width on desktop, width on mobile')

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
