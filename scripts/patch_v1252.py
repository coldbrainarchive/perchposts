#!/usr/bin/env python3
"""Patch v1251 -> v1252: Flock's icon is a black outline of the base bird every user's picture is built from
(_deploy/birds/songbird.png), traced and smoothed: round head, beak wedge pointing down-left with its seam line, eye."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1251.js'
dst = '_deploy/assets/index-DUcNPOLc-v1252.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
def body(s): return s.replace('"', '\\"')
patch(body('<path d="M6.3 9.2A7.5 7.5 0 1 1 9 18"/><path d="M6.3 9.2 2.5 11l4 1.6"/><path d="M6.5 12.6C6.8 15 7.6 16.8 9 18"/><path d="M10.5 9.3h.01"/>'),
      body('<path d="M5.6 11C6 6 9.5 3.3 13.8 3.3c5.2 0 8.9 3.7 8.9 8.7s-3.7 8.7-8.5 8.7c-2.7 0-5-.9-6.6-2.5L1.5 16.9c1-2.6 2.3-4.5 4.1-5.9z"/><path d="M5.6 11c1.2 2 2 4.5 2 7.2"/><circle cx="10.6" cy="11" r="1.3" fill="currentColor" stroke="none"/>'), 'traced user bird')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
