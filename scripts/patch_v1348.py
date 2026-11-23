#!/usr/bin/env python3
"""Patch v1347 -> v1348: tapping the globe logo opens the trending globe page (/globe/, a separate static page with
its own 3D library). Tapping the site name (or its countdown) still goes home."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1347.js'
dst = '_deploy/assets/index-DUcNPOLc-v1348.js'
c = open(src, encoding='utf-8').read()
old = "(0,L.jsx)(`span`,{className:`pp-logo`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppLogo(`glow`)}})"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "(0,L.jsx)(`span`,{className:`pp-logo`,role:`link`,\"aria-label\":`Trending globe`,title:`Trending around the world`,onClick:ev=>{ev.preventDefault();ev.stopPropagation();location.href=`/globe/`},style:{cursor:`pointer`},dangerouslySetInnerHTML:{__html:_ppLogo(`glow`)}})")
open(dst, 'w', encoding='utf-8').write(c); print('OK, wrote', dst)
