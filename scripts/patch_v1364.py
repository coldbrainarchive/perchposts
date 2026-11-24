#!/usr/bin/env python3
"""Patch v1363 -> v1364: bigger post picture in the chat header (30px -> 40px)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1363.js'
dst = '_deploy/assets/index-DUcNPOLc-v1364.js'
c = open(src, encoding='utf-8').read()
old = "body .lb-ic{"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "body .ch-bar .ch-th{width:40px;height:40px;border-radius:10px}body .lb-ic{")
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
