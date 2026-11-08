#!/usr/bin/env python3
"""Patch v869 -> v870: badges level with the tags, and the same space above the tags as below the buttons.
Desktop measured: tags 20px from the card top, buttons 18px from the bottom, badges centred 5px above the
tags. Phone: 15px top, 14px bottom, badges already level. Desktop top padding 18 -> 16 and badges top 14 -> 17
make it 18/18 with the badges centred on the tags; phone bottom padding 13 -> 14 makes it 15/15.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v869.js'
dst = '_deploy/assets/index-DUcNPOLc-v870.js'

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

patch('padding: 18px 20px 17px;', 'padding: 16px 20px 17px;', 'desktop top space')
patch('.feed-post-card>.post-badges{right:20px!important}', '.feed-post-card>.post-badges{right:20px!important;top:17px!important}', 'desktop badges level')
patch('.feed-post-card {\n          padding: 14px 14px 13px;\n        }\n\n        .feed-post-card > .post-badges {\n          right: 14px !important;\n        }',
      '.feed-post-card {\n          padding: 14px 14px 14px;\n        }\n\n        .feed-post-card > .post-badges {\n          right: 14px !important;\n          top: 14px !important;\n        }', 'phone bottom space')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
