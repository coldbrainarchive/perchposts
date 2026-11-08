#!/usr/bin/env python3
"""Patch v850 -> v851: the 🤖 gets its own centring. Its antenna makes it taller, so the shared nudge left it
0.85px high and 0.34px right on a real iPhone. Padding moves a centred item by half its size.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v850.js'
dst = '_deploy/assets/index-DUcNPOLc-v851.js'

content = open(src, encoding='utf-8').read()
old = '@supports (-webkit-touch-callout:none){.post-badge{padding:0 0 .7px 1.4px}}'
new = ('.post-badge.bot{padding:1px 0 0 3px}'
       '@supports (-webkit-touch-callout:none){.post-badge{padding:0 0 .7px 1.4px}.post-badge.bot{padding:1px 0 0 .7px}}')
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old)))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
