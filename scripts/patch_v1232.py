#!/usr/bin/env python3
"""Patch v1231 -> v1232: the "↑ N NEW POSTS" pill is tag-pill size (22px tall, 10px heavy uppercase, 0 9px padding),
like the GENERAL / country tags and user pills. In the post scroller it sits centred on the ‹ button row."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1231.js'
dst = '_deploy/assets/index-DUcNPOLc-v1232.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("gap:6px;height:36px;padding:0 16px;", "gap:4px;height:22px;padding:0 9px;", 'tag-pill height')
patch("font-weight:800;font-size:13px;line-height:1;letter-spacing:.06em;text-transform:uppercase;box-shadow:0 6px 20px rgba(0,0,0,.45);",
      "font-weight:800;font-size:10px;line-height:1;letter-spacing:.3px;text-transform:uppercase;box-shadow:0 3px 10px rgba(0,0,0,.45);", 'tag-pill text')
patch("transform:translate(-50%,-14px)", "transform:translate(-50%,-8px)", 'smaller drop-in')
patch("body:has(.reel) .pp-newpill{top:var(--pp-np-reel,calc(22px + env(safe-area-inset-top)));height:38px;z-index:9600}",
      "body:has(.reel) .pp-newpill{top:var(--pp-np-reel,calc(30px + env(safe-area-inset-top)));z-index:9600}", 'scroller: same small size')
# centre the 22px pill on the 38px ‹ button
patch("el.style.setProperty(`--pp-np-reel`,rx.getBoundingClientRect().top+`px`)",
      "el.style.setProperty(`--pp-np-reel`,(rx.getBoundingClientRect().top+(rx.getBoundingClientRect().height-22)/2)+`px`)", 'centre on the ‹ row')
patch('width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.6"', 'width="11" height="11" fill="none" stroke="currentColor" stroke-width="3"', 'smaller arrow')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
