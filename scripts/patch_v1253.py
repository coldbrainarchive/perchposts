#!/usr/bin/env python3
"""Patch v1252 -> v1253: bigger eye on Flock's traced bird icon (r 1.3 -> 2.2)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1252.js'
dst = '_deploy/assets/index-DUcNPOLc-v1253.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('<circle cx=\\"10.6\\" cy=\\"11\\" r=\\"1.3\\" fill=\\"currentColor\\" stroke=\\"none\\"/>',
      '<circle cx=\\"11\\" cy=\\"11\\" r=\\"2.2\\" fill=\\"currentColor\\" stroke=\\"none\\"/>', 'bigger eye')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
