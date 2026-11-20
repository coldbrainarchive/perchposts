#!/usr/bin/env python3
"""Patch v1264 -> v1265: chirp mod/admin globe sized to the 11px name text (0.9em = ~10px) instead of 14px."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1264.js'
dst = '_deploy/assets/index-DUcNPOLc-v1265.js'
c = open(src, encoding='utf-8').read()
old = "body .pp-chirp-globe{display:inline-flex;width:14px;height:14px;flex-shrink:0;color:#0a0a0a}body .pp-chirp-globe svg{width:14px;height:14px;stroke-width:2.4}"
new = "body .pp-chirp-globe{display:inline-flex;font-size:11px;width:.9em;height:.9em;flex-shrink:0;color:#0a0a0a}body .pp-chirp-globe svg{width:100%;height:100%;stroke-width:2.6}"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, new); print('OK: size')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
