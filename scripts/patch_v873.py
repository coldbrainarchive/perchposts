#!/usr/bin/env python3
"""Patch v872 -> v873: all four vertical gaps in a feed card are 11px, on desktop and phone, as asked
(card top -> tags, tags -> post box, post box -> buttons, buttons -> card bottom). The pin/lock badges move
with the tags so they stay centred on them.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v872.js'
dst = '_deploy/assets/index-DUcNPOLc-v873.js'

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

# desktop: tags sit 1px inside their row, so padding and row margin are 1px less than 11
patch('padding: 16px 20px 17px;', 'padding: 10px 20px 11px;', 'desktop card padding')
patch('.feed-post-card>.post-badges{right:20px!important;top:17px!important}', '.feed-post-card>.post-badges{right:20px!important;top:11px!important}', 'desktop badges')
patch('.feed-post-card>.feed-post-board-row{margin-bottom:16px!important}', '.feed-post-card>.feed-post-board-row{margin-bottom:10px!important}', 'desktop tags gap')
patch('.feed-post-card>.feed-post-actions{margin-top:17px!important}', '.feed-post-card>.feed-post-actions{margin-top:11px!important}', 'desktop buttons gap')
# phone
patch('.feed-post-card {\n          padding: 14px 14px 14px;\n        }', '.feed-post-card {\n          padding: 11px 14px 11px;\n        }', 'phone card padding')
patch('right: 14px !important;\n          top: 14px !important;', 'right: 14px !important;\n          top: 11px !important;', 'phone badges')
patch('.feed-post-card > .feed-post-board-row {\n          margin-bottom: 14px !important;', '.feed-post-card > .feed-post-board-row {\n          margin-bottom: 11px !important;', 'phone tags gap')
patch('.feed-post-card > .feed-post-actions {\n          margin-top: 14px !important;', '.feed-post-card > .feed-post-actions {\n          margin-top: 11px !important;', 'phone buttons gap')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
