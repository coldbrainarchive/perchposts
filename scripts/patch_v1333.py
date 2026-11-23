#!/usr/bin/env python3
"""Patch v1332 -> v1333: Tags dropdown label says "Popular flock tags" (drops "this week")."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1332.js'
dst = '_deploy/assets/index-DUcNPOLc-v1333.js'
c = open(src, encoding='utf-8').read()
old = "children:`Popular flock tags this week`"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "children:`Popular flock tags`"); print('OK: label')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
