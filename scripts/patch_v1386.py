#!/usr/bin/env python3
"""Patch v1385 -> v1386: scroller see-through pieces a little more transparent (.72 -> .55)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1385.js'
dst = '_deploy/assets/index-DUcNPOLc-v1386.js'
c = open(src, encoding='utf-8').read()
old = "body .reel-gmu,body .reel .reel-hint,body .reel-count,body .reel .reel-m .reel-count{background:rgba(35,38,46,.72)!important}"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, old.replace(".72)", ".55)")); print('OK')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
