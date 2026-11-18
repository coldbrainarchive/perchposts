#!/usr/bin/env python3
"""Patch v1205 -> v1206 (scroller, media slides):
- No shading on the title, pills or VIEW POST (the text shadows / glow and the pills' tint are gone; the text layer
  no longer gets its own compositing layer, which could show as a shaded box on iPhones).
- The flaps bar and the name / title / VIEW POST cluster sit higher, clear of Safari's bottom address bar
  (bar 28px + safe area from the bottom; the 15px gaps stay); the bottom fade sits under them."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1205.js'
dst = '_deploy/assets/index-DUcNPOLc-v1206.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
css = ("body .reel .reel-m .reel-title,body .reel .reel-m .reel-head .reel-tag,body .reel .reel-m a.reel-site,body .reel .reel-m .reel-head .reel-tag *{text-shadow:none!important}"
       "body .reel .reel-m .reel-head .reel-tag{background:transparent!important}"
       "body .reel .reel-m .reel-inner>:not(.reel-media){transform:none!important;will-change:auto!important}"
       "body .reel .reel-dock{bottom:calc(28px + env(safe-area-inset-bottom))!important}"
       "body .reel .reel-slide.reel-m{padding-bottom:calc(77px + env(safe-area-inset-bottom))!important}"
       "body .reel-view{-webkit-mask-image:linear-gradient(to bottom,transparent 0,rgba(0,0,0,.35) calc(30px + env(safe-area-inset-top)),#000 calc(110px + env(safe-area-inset-top)),#000 calc(100% - 66px - env(safe-area-inset-bottom)),rgba(0,0,0,.35) calc(100% - 22px - env(safe-area-inset-bottom)),transparent 100%)!important;"
       "mask-image:linear-gradient(to bottom,transparent 0,rgba(0,0,0,.35) calc(30px + env(safe-area-inset-top)),#000 calc(110px + env(safe-area-inset-top)),#000 calc(100% - 66px - env(safe-area-inset-bottom)),rgba(0,0,0,.35) calc(100% - 22px - env(safe-area-inset-bottom)),transparent 100%)!important}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
