#!/usr/bin/env python3
"""Patch v813 -> v814: the chirp pill in the chat header is a size up from the small action pills
(26px tall, 13px text, on phone and desktop), since it now works as the chat's heading.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v813.js'
dst = '_deploy/assets/index-DUcNPOLc-v814.js'

content = open(src, encoding='utf-8').read()

old = '.comments-shell.chat-preview .chat-panel-header{padding:12px 14px 2px;border-bottom:none;background:none}'
new = old + '.comments-shell .chat-panel-header .feed-post-action-pill{height:26px;padding:0 10px;font-size:13px}'
if content.count(old) != 1:
    print('FAIL: expected 1 match, found ' + str(content.count(old)))
    sys.exit(1)
content = content.replace(old, new)
print('OK: bigger pill')
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
