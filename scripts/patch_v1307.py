#!/usr/bin/env python3
"""Patch v1306 -> v1307: the Worm wallet opened from the post scroller is black with a fine top edge (like the Share
sheet there); its colour tail below the sheet is black too. Elsewhere it keeps its grey."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1306.js'
dst = '_deploy/assets/index-DUcNPOLc-v1307.js'
c = open(src, encoding='utf-8').read()
old = "html.reel-shown .ww-ov{z-index:9800!important}"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, old + "html.reel-shown .ww-ov .ww-sheet{background:#000!important;border-top:1px solid #2a2d36;box-shadow:0 -10px 40px rgba(0,0,0,.45),0 300px 0 0 #000!important}html.reel-shown .ww-ov .ww-in{background:#0d0f14}"); print('OK')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
