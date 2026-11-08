#!/usr/bin/env python3
"""Patch v866 -> v867: line up the post badges (pin, lock, bot) with the card's content edge.
The badges sat a fixed 16px in from the card edge, but the card's padding is 20px on desktop and 14px on
phones, so on desktop they stuck out about 4px past the post box and the time pill. They now use the same
inset as the padding at each size.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v866.js'
dst = '_deploy/assets/index-DUcNPOLc-v867.js'

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

def t(s):
    return s.replace('`', q)

patch('.feed-post-card:has(.post-badges>:nth-child(1)) .feed-post-board-row{padding-right:28px}',
      '.feed-post-card>.post-badges{right:20px!important}.feed-post-card:has(.post-badges>:nth-child(1)) .feed-post-board-row{padding-right:28px}',
      'desktop badge inset')
patch('.feed-post-card {\n          padding: 14px 14px 13px;\n        }',
      '.feed-post-card {\n          padding: 14px 14px 13px;\n        }\n\n        .feed-post-card > .post-badges {\n          right: 14px !important;\n        }',
      'phone badge inset')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
