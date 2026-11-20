#!/usr/bin/env python3
"""Patch v1254 -> v1255: thicker lines on the Perch News globe to match the other space icons' weight
(ring 11, grid 9; one meridian instead of two so the thicker lines don't fill in at tag size)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1254.js'
dst = '_deploy/assets/index-DUcNPOLc-v1255.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
old = ('<defs><clipPath id="pnbcc"><circle cx="50" cy="50" r="44"/></clipPath></defs>'
     '<g fill="none" stroke="#0a0a0a"><circle cx="50" cy="50" r="44" stroke-width="7"/><line x1="6" y1="50" x2="94" y2="50" stroke-width="6"/>'
     '<path d="M 14 28 Q 50 38 86 28" stroke-width="6"/><path d="M 14 72 Q 50 62 86 72" stroke-width="6"/>'
     '<ellipse cx="50" cy="50" rx="16" ry="44" stroke-width="6" clip-path="url(#pnbcc)"/><ellipse cx="50" cy="50" rx="32" ry="44" stroke-width="6" clip-path="url(#pnbcc)"/></g>')
new = ('<defs><clipPath id="pnbcc"><circle cx="50" cy="50" r="42"/></clipPath></defs>'
     '<g fill="none" stroke="#0a0a0a" stroke-linecap="round" clip-path="url(#pnbcc)"><line x1="0" y1="50" x2="100" y2="50" stroke-width="9"/>'
     '<path d="M 0 26 Q 50 40 100 26" stroke-width="9"/><path d="M 0 74 Q 50 60 100 74" stroke-width="9"/>'
     '<ellipse cx="50" cy="50" rx="20" ry="42" stroke-width="9"/></g><circle cx="50" cy="50" r="42" fill="none" stroke="#0a0a0a" stroke-width="11"/>')
patch(old, new, 'thicker globe')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
