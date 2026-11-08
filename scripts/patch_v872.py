#!/usr/bin/env python3
"""Patch v871 -> v872: the four vertical gaps in a feed card are the same, as asked:
card top -> tags, tags -> post box, post box -> buttons, buttons -> card bottom.
Measured before: desktop 17/11/13/17, phone 14/10/11/14. Now 17/17/17/17 and 14/14/14/14.
The tag row is 1px taller than its tags on desktop, so its margin is 1px less there.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v871.js'
dst = '_deploy/assets/index-DUcNPOLc-v872.js'

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

patch('.feed-post-card>.post-badges{right:20px!important;top:17px!important}',
      '.feed-post-card>.post-badges{right:20px!important;top:17px!important}'
      '.feed-post-card>.feed-post-board-row{margin-bottom:16px!important}'
      '.feed-post-card>.feed-post-board-row+*{margin-top:0!important}'
      '.feed-post-card>.feed-post-actions{margin-top:17px!important}',
      'desktop gaps')
patch('.feed-post-card > .post-badges {\n          right: 14px !important;\n          top: 14px !important;\n        }',
      '.feed-post-card > .post-badges {\n          right: 14px !important;\n          top: 14px !important;\n        }\n\n'
      '        .feed-post-card > .feed-post-board-row {\n          margin-bottom: 14px !important;\n        }\n\n'
      '        .feed-post-card > .feed-post-actions {\n          margin-top: 14px !important;\n        }',
      'phone gaps')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
