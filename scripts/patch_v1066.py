#!/usr/bin/env python3
"""Patch v1065 -> v1066: logo grid lines inside the globe made thinner (1.6 instead of 3.6), so the face reads first.
Artwork: brand/bird-globe-glow.svg (previous: brand/bird-globe-glow-v1061.svg)."""
import sys, json, re
src = '_deploy/assets/index-DUcNPOLc-v1065.js'
dst = '_deploy/assets/index-DUcNPOLc-v1066.js'
c = open(src, encoding='utf-8').read()
i = c.find('function _ppLogo(kind,col){const S=')
assert i >= 0 and c.count('function _ppLogo(kind,col){const S=') == 1
j = c.find(';if(kind===`mono`)', i)
S = json.loads(c[i + len('function _ppLogo(kind,col){const S='):j])
S['glow'] = open('brand/bird-globe-glow.svg').read()
c = c[:i] + 'function _ppLogo(kind,col){const S=' + json.dumps(S) + c[j:]
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
