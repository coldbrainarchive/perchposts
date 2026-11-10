#!/usr/bin/env python3
"""Patch v963 -> v964: one background colour for the open chat on phones. The chat told Safari its colour was
#16171d (theme-color) while the chat is #14161c and an old compose rule said #13151c, so Safari's toolbar
strip under the message box came out a shade off. All three are #14161c now."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v963.js'
dst = '_deploy/assets/index-DUcNPOLc-v964.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('_tc&&(_tc.content=`#16171d`);_h.classList.add(`chat-open`);', '_tc&&(_tc.content=`#14161c`);_h.classList.add(`chat-open`);', 'theme-color in chat')
patch('padding: 10px 12px 14px;\n        gap: 5px;\n        background: #13151c;', 'padding: 10px 12px 14px;\n        gap: 5px;\n        background: #14161c;', 'compose colour')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
