#!/usr/bin/env python3
"""Patch v1370 -> v1371: the chirps go back to their old colour (v1369's black removed; the hidden "new posts" pill
stays), and the post scroller (preview) takes the main page's colour (#16171d) instead of black — page, fades over
photos/videos, its sheets, and Safari's bar colour — to see how it looks."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1370.js'
dst = '_deploy/assets/index-DUcNPOLc-v1371.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
G = '#16171d'; R = '22,23,29'
patch("_tc.content=`#000000`", "_tc.content=`#14161c`", 'chat theme back')
patch("html.chat-open.chat-open,html.chat-open.chat-open body{background:#000!important}html.chat-open.chat-open body::after{background:#000!important}"
      "body .comments-shell.chat-full{background:#000}"
      "body .comments-shell.chat-full .chat-panel-header{background:#000;border-bottom:1px solid #2a2d36}"
      "body .chat-full .chat-panel-header{border-top-color:#000}"
      "body .comments-shell.chat-full .chat-compose{background:#000;border-top:1px solid #2a2d36}"
      "body .comments-shell.chat-full .chat-window{background:#000}"
      "body .chat-full .chp,body .chat-full .chp.chp-full{background:#000;border-bottom:1px solid #2a2d36}", "", 'chat colours back')
patch("tcm&&tcm.setAttribute(`content`,`#000000`);document.documentElement.classList.add(`reel-shown`);",
      f"tcm&&tcm.setAttribute(`content`,`{G}`);document.documentElement.classList.add(`reel-shown`);", 'reel theme colour')
patch("body .lb-ic{",
 f"html.reel-shown.reel-shown.reel-shown,html.reel-shown.reel-shown.reel-shown body,html.ps-kb.reel-shown.reel-shown,html.ps-kb.reel-shown.reel-shown body{{background:{G}!important}}"
 f"body .reel.reel{{background:{G}!important}}"
 f"body .reel .reel-fade-t{{background:linear-gradient(to bottom,{G} 0%,rgba({R},.75) 28%,rgba({R},.3) 65%,rgba({R},0) 100%)!important}}"
 f"body .reel .reel-fade-b{{background:linear-gradient(to top,{G} 0%,rgba({R},.85) 45%,rgba({R},0) 100%)!important}}"
 f"body .reel.reel .reel-m .reel-media{{background:{G}!important}}"
 f"body .reel.reel .reel-m::after{{background:linear-gradient(to top,{G} 0%,rgba({R},.82) 9%,rgba({R},.55) 24%,rgba({R},0) 48%),linear-gradient(to bottom,{G} 0%,rgba({R},.65) 7%,rgba({R},0) 20%)!important}}"
 f"html.reel-shown .ps-sheet,html.reel-shown .ww-ov .ww-sheet{{background:{G}!important}}"
 "body .lb-ic{", 'reel colours')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
