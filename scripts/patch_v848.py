#!/usr/bin/env python3
"""Patch v847 -> v848: nudge the emoji in post badges to true centre. Emojis draw off-centre inside their own
character box, by a different amount per browser: measured 1.5px left in desktop Chrome, and 0.7px left and
0.3px low on iPhone (from a real screenshot). Padding moves a centred item by half its size.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v847.js'
dst = '_deploy/assets/index-DUcNPOLc-v848.js'

content = open(src, encoding='utf-8').read()
old = 'text-align:center;flex-shrink:0;box-sizing:border-box;padding:0}'
new = ('text-align:center;flex-shrink:0;box-sizing:border-box;padding:0 0 0 3px}'
       '@supports (-webkit-touch-callout:none){.post-badge{padding:0 0 .7px 1.4px}}')
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old)))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
