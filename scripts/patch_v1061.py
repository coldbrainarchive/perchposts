#!/usr/bin/env python3
"""Patch v1060 -> v1061: header logo tuned for small sizes: bigger eye, beak and crest (~30%), and the eye is a ring
with a small purple dot up and to the right. Artwork: brand/bird-globe-glow.svg (previous: brand/bird-globe-glow-v1059.svg)."""
import sys, json, re
src = '_deploy/assets/index-DUcNPOLc-v1060.js'
dst = '_deploy/assets/index-DUcNPOLc-v1061.js'
c = open(src, encoding='utf-8').read()
i = c.find('function _ppLogo(kind,col){const S=')
assert i >= 0 and c.count('function _ppLogo(kind,col){const S=') == 1
j = c.find(';if(kind===`mono`)', i)
S = json.loads(c[i + len('function _ppLogo(kind,col){const S='):j])
S['glow'] = open('brand/bird-globe-glow.svg').read()
c = c[:i] + 'function _ppLogo(kind,col){const S=' + json.dumps(S) + c[j:]
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
