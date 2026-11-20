#!/usr/bin/env python3
"""Patch v1287 -> v1288: no arrow on the website link of link posts in the post scroller (View post keeps its arrow)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1287.js'
dst = '_deploy/assets/index-DUcNPOLc-v1288.js'
c = open(src, encoding='utf-8').read()
old = "body .reel-site-up{margin-top:8px}"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, old + "body .reel-site-up .reel-site-ar{display:none}"); print('OK: hide arrow')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
