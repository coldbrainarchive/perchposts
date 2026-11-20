#!/usr/bin/env python3
"""Patch v1291 -> v1292: link posts in the post scroller: the website link sits above the title (was below it)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1291.js'
dst = '_deploy/assets/index-DUcNPOLc-v1292.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("if(tt){tt.after(site);site.classList.add(`reel-site-up`)}", "if(tt){tt.before(site);site.classList.add(`reel-site-up`)}", 'link above title')
patch("body .reel-site-up{margin-top:8px}", "body .reel-site-up{margin-top:0!important;margin-bottom:2px}", 'spacing')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
