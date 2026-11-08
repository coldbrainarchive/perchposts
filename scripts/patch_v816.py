#!/usr/bin/env python3
"""Patch v815 -> v816: on phones a huddle opens on its post page, like any other post, instead of
going straight into the full chat. Notifications (highlight, nc, sy) still open the chat at the chirp.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v815.js'
dst = '_deploy/assets/index-DUcNPOLc-v816.js'

content = open(src, encoding='utf-8').read()

old = '_first&&(c.is_huddle||te.current)'
new = '_first&&te.current'
if content.count(old) != 1:
    print('FAIL: expected 1 match, found ' + str(content.count(old)))
    sys.exit(1)
content = content.replace(old, new)
print('OK: huddles open on the post page')
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
