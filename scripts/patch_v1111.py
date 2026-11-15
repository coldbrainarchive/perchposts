#!/usr/bin/env python3
"""Patch v1110 -> v1111: sign-up nest eggs each get their own look from the name (plain, fine speckles, blotches, ring of spots, scribbles, mixed), in the bird's colours or dark speckles; no two alike in a nest."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1110.js'
dst = '_deploy/assets/index-DUcNPOLc-v1111.js'
c = open(src, encoding='utf-8').read()
H = '/*ppnest*/'
a = c.index(H) + len(H); w = c.index('function _PNest(', a)
c = c[:a] + open('birds/nest.js', encoding='utf-8').read() + '\n' + c[w:]; print('OK: nest code updated')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
