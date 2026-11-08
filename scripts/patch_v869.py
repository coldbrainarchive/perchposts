#!/usr/bin/env python3
"""Patch v868 -> v869: no emoji nudge in the post badges outside Apple's own browsers.
The 3px left padding from v848 was measured in headless Chrome, which draws emoji differently from the real
browser. Measured in a real Chrome 156 window on a Retina Mac: with the nudge 📌 🔒 🤖 sit 1.25-1.75px right,
without it they are within 0.25px of centre (matches the user's screenshot). At 1x real Chrome snaps the
emoji to whole pixels, so the padding makes no difference there. iPhone and Mac Safari keep their own
@supports rules, which come later and still override this. The v868 resolution-only rule is no longer needed.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v868.js'
dst = '_deploy/assets/index-DUcNPOLc-v869.js'

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

patch('@media (max-resolution:1.49dppx){.post-badge,.post-badge.bot{padding:0!important}.post-badge-i{transform:none!important}}', '', 'drop the 1x-only rule')
patch('box-sizing:border-box;padding:0 0 0 3px}', 'box-sizing:border-box;padding:0}', 'no default nudge')
patch('.post-badge.bot{padding:0 0 0 3px}', '.post-badge.bot{padding:0}', 'no default bot nudge')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
