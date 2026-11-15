#!/usr/bin/env python3
"""Patch v1087 -> v1088: the chosen-name box on sign-up is filled with the bird colour again, like the username pill (bigger eggs stay)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1087.js'
dst = '_deploy/assets/index-DUcNPOLc-v1088.js'
c = open(src, encoding='utf-8').read()
H, T = '/*ppnest*/', '/*/ppnest*/'
i, j = c.index(H) + len(H), c.index(T)
w = c.index('function _PNest(', i)
c = c[:i] + open('birds/nest.js', encoding='utf-8').read() + '\n' + c[w:]; print('OK: nest code updated')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
