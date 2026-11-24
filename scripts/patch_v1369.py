#!/usr/bin/env python3
"""Patch v1365 -> v1369 (v1366–v1368's Safari-strip attempts dropped at the user's request):
- The chat screen is black like the post scroller (page, header, message bar, drop-down; same #2a2d36 dividers),
  so the strip under Safari's toolbar matches whichever way it lags.
- The scroller's "N new posts" pill no longer floats over the chat (kept from v1367)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1365.js'
dst = '_deploy/assets/index-DUcNPOLc-v1369.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("_tc.content=`#14161c`", "_tc.content=`#000000`", 'theme-color black in chat')
patch("body .lb-ic{",
 "html.chat-open.chat-open,html.chat-open.chat-open body{background:#000!important}html.chat-open.chat-open body::after{background:#000!important}"
 "body .comments-shell.chat-full{background:#000}"
 "body .comments-shell.chat-full .chat-panel-header{background:#000;border-bottom:1px solid #2a2d36}"
 "body .chat-full .chat-panel-header{border-top-color:#000}"
 "body .comments-shell.chat-full .chat-compose{background:#000;border-top:1px solid #2a2d36}"
 "body .comments-shell.chat-full .chat-window{background:#000}"
 "body .chat-full .chp,body .chat-full .chp.chp-full{background:#000;border-bottom:1px solid #2a2d36}"
 "html.chat-open .pp-newpill{display:none!important}"
 "body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
