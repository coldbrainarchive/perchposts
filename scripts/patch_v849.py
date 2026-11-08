#!/usr/bin/env python3
"""Patch v848 -> v849: the flap pill had 1px more space on its left than its right, measured from a real
iPhone screenshot. Every other pill was already within half a pixel, so nothing else changes.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v848.js'
dst = '_deploy/assets/index-DUcNPOLc-v849.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

BG = '{borderColor:`#c084fc`,background:`rgba(192,132,252,0.15)`,paddingLeft:'.replace('`', q)
patch('style:r===1&&i?' + BG + '5}:{paddingLeft:5},', 'style:r===1&&i?' + BG + '4}:{paddingLeft:4},', 'feed card')
patch('style:re.myVote===1?' + BG + '5}:{paddingLeft:5},', 'style:re.myVote===1?' + BG + '4}:{paddingLeft:4},', 'post page')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
