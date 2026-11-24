#!/usr/bin/env python3
"""Patch v1366 -> v1367 (iPhone Safari, from the user's screen recording):
- Swiping back from a chat into the post scroller left the strip under Safari's bottom toolbar grey: Safari kept
  painting the page colour it had there (the feed's grey) after the scroller turned the page black. The scroller now
  paints its own black strip below the screen edge (a fixed block under the toolbar), so it no longer relies on Safari.
- Undo v1366's theme-color tag swap (it didn't help, and it broke the scroller restoring the colour when closing).
- The scroller's "N new posts" pill no longer floats over the chat."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1366.js'
dst = '_deploy/assets/index-DUcNPOLc-v1367.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("_h.classList.remove(`chat-open`,`chat-kb`,`chat-crios`);_ppTcKick();", "_h.classList.remove(`chat-open`,`chat-kb`,`chat-crios`);", 'undo tc kick')
patch("body .lb-ic{",
 "html.reel-shown body::after{content:\"\";position:fixed;left:0;right:0;top:100%;height:70vh;background:#000;pointer-events:none;z-index:9499}"
 "html.chat-open .pp-newpill{display:none!important}"
 "body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
