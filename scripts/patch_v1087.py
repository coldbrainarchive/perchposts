#!/usr/bin/env python3
"""Patch v1086 -> v1087: sign-up nest: eggs 20% bigger (nest a little bigger to hold them), and the chosen-name box styled like the profile card."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1086.js'
dst = '_deploy/assets/index-DUcNPOLc-v1087.js'
c = open(src, encoding='utf-8').read()
H, T = '/*ppnest*/', '/*/ppnest*/'
i, j = c.index(H) + len(H), c.index(T)
w = c.index('function _PNest(', i)
c = c[:i] + open('birds/nest.js', encoding='utf-8').read() + '\n' + c[w:]; print('OK: nest code updated')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
