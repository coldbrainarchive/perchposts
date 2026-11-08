#!/usr/bin/env python3
"""Patch v853 -> v854: centre the 🤖 by the smallest circle that fits around it, the user's idea. A bounding box
gets skewed by the thin antenna, a fitted circle doesn't. iPhone: that circle measured 0.33px left and 0.34px
low of the badge's centre, from a real close-up, so the transform moves by the opposite.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v853.js'
dst = '_deploy/assets/index-DUcNPOLc-v854.js'
DX, DY = sys.argv[1], sys.argv[2]

content = open(src, encoding='utf-8').read()
import re
m = re.search(r'\.post-badge-i\{display:block;transform:translateY\(([-.\d]+)px\)\}', content)
if not m:
    print('FAIL desktop rule'); sys.exit(1)
content = content.replace(m.group(0), '.post-badge-i{display:block;transform:translate(' + DX + 'px,' + DY + 'px)}')
old = '.post-badge-i{transform:translate(-.25px,-.77px)}'
if content.count(old) != 1:
    print('FAIL iphone rule'); sys.exit(1)
content = content.replace(old, '.post-badge-i{transform:translate(.08px,-1.11px)}')
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
