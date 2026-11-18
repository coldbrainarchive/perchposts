#!/usr/bin/env python3
"""Patch v1198 -> v1199 (scroller):
- The "Swipe up for the next post" hint is white text in a dark see-through pill, so it shows on any photo.
- Full-screen media slides: the name / tags / title / VIEW POST block is tighter and sits closer to the flaps bar
  (smaller gaps, title 19px and at most 2 lines)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1198.js'
dst = '_deploy/assets/index-DUcNPOLc-v1199.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
css = ("body .reel .reel-hint{color:#fff!important;text-shadow:none}"
       "body .reel .reel-hint .reel-hint-t,body .reel .reel-hint .reel-arrow{display:inline-flex;align-items:center}"
       "body .reel .reel-hint{left:50%;transform:translateX(-50%);padding:6px 14px;border-radius:999px;background:rgba(0,0,0,.55);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);gap:6px;font-weight:700}"
       "body .reel .reel-hint .reel-arrow{color:#fff}body .reel .reel-hint.end{color:#86efac!important}body .reel .reel-hint.end .reel-arrow{color:#86efac}"
       "body .reel .reel-slide.reel-m{padding-bottom:calc(64px + env(safe-area-inset-bottom))!important}"
       "body .reel .reel-m .reel-head{margin-bottom:5px!important}"
       "body .reel .reel-m .reel-title{font-size:19px!important;line-height:1.25!important;margin-top:0!important;-webkit-line-clamp:2!important}"
       "body .reel .reel-m a.reel-site{margin-top:2px!important;padding:3px 0!important}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
