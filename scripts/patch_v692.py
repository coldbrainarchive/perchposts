#!/usr/bin/env python3
"""Patch v691 -> v692:
Fix lightbox image squishing/stretching on mobile.
Problem: forcing width:92vw then capping height with max-height breaks aspect ratio
when both constraints are active (very portrait images on mobile with toolbar visible).
Fix: use max-width:92vw + max-height (no forced width). The browser maintains
aspect ratio correctly when only max constraints are set — the image scales down
proportionally to satisfy whichever limit is hit first.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v691.js'
dst = '_deploy/assets/index-DUcNPOLc-v692.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

old_im = (q + "${window.innerWidth>=768?'max-width':'width'}:92vw;height:auto;"
          "max-height:${Math.round(_ih*0.88)}px;border-radius:10px;transition:opacity 0.2s;" + q)

new_im = (q + "max-width:92vw;max-height:${Math.round(_ih*0.88)}px;"
          "border-radius:10px;transition:opacity 0.2s;" + q)

n = content.count(old_im)
if n == 0:
    errors.append('FAIL: _im style not found')
else:
    content = content.replace(old_im, new_im)
    print(f'OK ({n}x): lightbox _im -> max-width only, no forced width (preserves AR)')

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
