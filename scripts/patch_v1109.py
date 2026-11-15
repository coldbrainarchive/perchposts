#!/usr/bin/env python3
"""Patch v1108 -> v1109: sign-up nest birds no longer turn around (it was a flat mirror flip). The four outer birds face
the middle of the nest; the middle one faces the way its name decides. Bobbing, head tilts, ducking and blinking stay."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1108.js'
dst = '_deploy/assets/index-DUcNPOLc-v1109.js'
c = open(src, encoding='utf-8').read()
H = '/*ppnest*/'
a = c.index(H) + len(H); w = c.index('function _PNest(', a)
c = c[:a] + open('birds/nest.js', encoding='utf-8').read() + '\n' + c[w:]; print('OK: nest code updated')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
