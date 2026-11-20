#!/usr/bin/env python3
"""Patch v1288 -> v1289: equal visible gaps in link posts in the scroller: website link -> text and text -> View post
(measured ink gaps were 28.7 vs 23 px; the text's top margin under the link goes 10px -> 4px)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1288.js'
dst = '_deploy/assets/index-DUcNPOLc-v1289.js'
c = open(src, encoding='utf-8').read()
old = "body .reel-site-up+.reel-descw,body .reel-site-up+.reel-desc{margin-top:10px}"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "body .reel-site-up+.reel-descw,body .reel-site-up+.reel-desc{margin-top:4px!important}"); print('OK')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
