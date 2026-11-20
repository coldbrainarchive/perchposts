#!/usr/bin/env python3
"""Patch v1248 -> v1249: Flock's bird head is now a round bird face looking left (like the bird emoji), with a tuft;
Sports gets a ball with curved seams (reads as baseball / tennis / basketball) instead of the football."""
import sys, re
src = '_deploy/assets/index-DUcNPOLc-v1248.js'
dst = '_deploy/assets/index-DUcNPOLc-v1249.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
def body(s): return s.replace('"', '\\"')
patch(body('<path d="M16.5 7A6 6 0 0 0 5 9.5c0 2.2 1 4 2.5 5L6 21h9.5c0-3 1-5 1-8.5"/><path d="M16.5 7 21.5 9.5l-5 1.5"/><path d="M12.5 8h.01"/>'),
      body('<circle cx="14" cy="12" r="7.5"/><path d="M6.8 10 2.5 12.3l4.6 1.2"/><path d="M11.5 10h.01"/><path d="M14 4.5c.5-1.5 2-2.3 3.5-2"/>'), 'round bird head')
patch(body('<ellipse cx="12" cy="12" rx="10.5" ry="6" transform="rotate(-45 12 12)"/><path d="M9 15l6-6"/><path d="M11 11.5l1.5 1.5"/>'),
      body('<circle cx="12" cy="12" r="9.5"/><path d="M6 4.6a12 12 0 0 1 0 14.8"/><path d="M18 4.6a12 12 0 0 0 0 14.8"/>'), 'sports ball')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
