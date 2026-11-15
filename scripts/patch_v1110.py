#!/usr/bin/env python3
"""Patch v1109 -> v1110: flap / chirp / share pills: the icon sits closer to its number or word (gap 6px+1px -> 3px)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1109.js'
dst = '_deploy/assets/index-DUcNPOLc-v1110.js'
c = open(src, encoding='utf-8').read()
old = "body .lb-ic{"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "body .feed-post-action-pill:has(.pp-ic){gap:3px}body .feed-post-action-pill .pp-ic{margin-right:0}" + old); print('OK: tighter icon spacing')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
