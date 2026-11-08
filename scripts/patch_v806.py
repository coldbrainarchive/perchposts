#!/usr/bin/env python3
"""Patch v805 -> v806:
Chrome on iPhone could stop scrolling short of the top of the page again. v804 made the page
scrollable while the chat is open, and the chat screen still set overscroll-behavior-y:none: the same
pairing that caused this bug before v797. Chrome on iOS no longer gets that setting. The message list
keeps its own overscroll:contain, and Safari is unchanged.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v805.js'
dst = '_deploy/assets/index-DUcNPOLc-v806.js'

content = open(src, encoding='utf-8').read()
old = 'html.chat-open,html.chat-open body{overscroll-behavior-y:none}'
new = 'html.chat-open:not(.chat-crios),html.chat-open:not(.chat-crios) body{overscroll-behavior-y:none}'
if content.count(old) != 1:
    print('FAIL: expected 1 match, found ' + str(content.count(old)))
    sys.exit(1)
content = content.replace(old, new)
print('OK: no overscroll lock for Chrome on iOS')
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
