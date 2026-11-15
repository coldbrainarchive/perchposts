#!/usr/bin/env python3
"""Patch v1096 -> v1097: sign-up nest: when the fresh-nest button shows, the hint line under it is hidden (the button takes its place)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1096.js'
dst = '_deploy/assets/index-DUcNPOLc-v1097.js'
c = open(src, encoding='utf-8').read()
H, T = '/*ppnest*/', '/*/ppnest*/'
i, j = c.index(H) + len(H), c.index(T)
w = c.index('function _PNest(', i)
c = c[:i] + open('birds/nest.js', encoding='utf-8').read() + '\n' + c[w:]; print('OK: nest code updated')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
