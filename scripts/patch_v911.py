#!/usr/bin/env python3
"""Patch v910 -> v911: header chips (New Post, Sign In, the notification count) match the board pills on
posts and in the dropdown: 22px tall, 10px text (were 20px / 9px). The bird button beside them was
already a 22px pill."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v910.js'
dst = '_deploy/assets/index-DUcNPOLc-v911.js'
content = open(src, encoding='utf-8').read()
reps = [
 ('box-sizing: border-box;\n        height: 20px;\n        padding: 0 7px;\n        border-radius: 999px;\n        background: #1f2937;\n        color: #f8fafc;\n        text-decoration: none;\n        font-size: 9px;',
  'box-sizing: border-box;\n        height: 22px;\n        padding: 0 7px;\n        border-radius: 999px;\n        background: #1f2937;\n        color: #f8fafc;\n        text-decoration: none;\n        font-size: 10px;'),
 ('.app-chip {\n          height: 20px;\n          padding: 0 7px;\n          font-size: 9px;\n        }',
  '.app-chip {\n          height: 22px;\n          padding: 0 7px;\n          font-size: 10px;\n        }'),
]
for o, n in reps:
    if content.count(o) != 1: print('FAIL', content.count(o), o[:60]); sys.exit(1)
    content = content.replace(o, n)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
