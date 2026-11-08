#!/usr/bin/env python3
"""Patch v867 -> v868: no emoji nudge in the post badges on standard-resolution screens.
The 3px left padding (v848) centres the emoji in Chrome on Retina screens, but on a 1x screen Chrome already
draws it centred, so the padding pushed 📌 🔒 🤖 about 1.5-2px right. Measured in desktop Chrome 156:
1x with nudge 1.5-2px right, 1x without nudge centred; 2x and 3x with nudge centred. Phones are always 2x or
more, so they are unaffected.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v867.js'
dst = '_deploy/assets/index-DUcNPOLc-v868.js'

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

patch('.feed-post-card>.post-badges{right:20px!important}',
      '.feed-post-card>.post-badges{right:20px!important}@media (max-resolution:1.49dppx){.post-badge,.post-badge.bot{padding:0!important}.post-badge-i{transform:none!important}}',
      'no nudge on 1x screens')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
