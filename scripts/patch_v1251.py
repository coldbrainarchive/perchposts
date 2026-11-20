#!/usr/bin/env python3
"""Patch v1250 -> v1251: Flock's icon goes back to just a bird's head, looking left like the users' bird
pictures: one simple round outline that runs into the beak, plus an eye."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1250.js'
dst = '_deploy/assets/index-DUcNPOLc-v1251.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
def body(s): return s.replace('"', '\\"')
patch(body('<path d="M6.8 7.5C7.3 4.8 9.3 3.6 11.3 4.2c2.2.7 2.9 3.2 1.9 5.8 3-.3 6-1.3 8.6-3.5-.3 6-3.5 11.3-9 12-4 .5-6.8-2-6.8-5.3 0-1.3.4-2.3 1-3.1"/><path d="M6.8 7.5 3 9.2l4 .7"/><path d="M9.6 7.4h.01"/><path d="M10.5 13.5c1.8 1.6 4.6 1.6 6.6-.6"/><path d="M10.5 18.6V21M13.5 18.3V21"/>'),
      body('<path d="M6.3 9.2A7.5 7.5 0 1 1 9 18"/><path d="M6.3 9.2 2.5 11l4 1.6"/><path d="M6.5 12.6C6.8 15 7.6 16.8 9 18"/><path d="M10.5 9.3h.01"/>'), 'bird head')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
