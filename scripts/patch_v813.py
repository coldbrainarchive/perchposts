#!/usr/bin/env python3
"""Patch v812 -> v813: months stop at 11, so times go 11mo ago -> 1y ago with no "12mo ago".
A month is 30 days, which reached 12 at day 360, five days before the year starts at day 365.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v812.js'
dst = '_deploy/assets/index-DUcNPOLc-v813.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()

old = '${Math.floor(n/2592e3)}mo ago'.replace('`', q)
new = '${Math.min(11,Math.floor(n/2592e3))}mo ago'.replace('`', q)
if content.count(old) != 1:
    print('FAIL: expected 1 match, found ' + str(content.count(old)))
    sys.exit(1)
content = content.replace(old, new)
print('OK: month cap')
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
