#!/usr/bin/env python3
"""Patch v1292 -> v1293: link posts in the scroller: photo -> website link and website link -> title are the same,
smaller visible gap (~14px each; were 31 and 20)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1292.js'
dst = '_deploy/assets/index-DUcNPOLc-v1293.js'
c = open(src, encoding='utf-8').read()
old = "body .reel-site-up{margin-top:0!important;margin-bottom:2px}"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "body .reel-site-up{margin-top:0!important;margin-bottom:-4px!important}body .reel-media+.reel-site-up{margin-top:-17px!important}"); print('OK')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
