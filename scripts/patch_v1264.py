#!/usr/bin/env python3
"""Patch v1263 -> v1264: the mod/admin globe next to names on chirps is the minimal Perch News globe (PNGLOBE).
The Bird ID badge keeps the detailed globe."""
import sys, re
src = '_deploy/assets/index-DUcNPOLc-v1263.js'
dst = '_deploy/assets/index-DUcNPOLc-v1264.js'
c = open(src, encoding='utf-8').read()
start = "f&&(0,L.jsxs)(`svg`,{width:`14`,height:`14`,viewBox:`0 0 100 100`"
end = "(0,L.jsx)(`clipPath`,{id:`bcc`,children:(0,L.jsx)(`circle`,{cx:`50`,cy:`50`,r:`44`})})]})"
if c.count(start) != 1 or c.count(end) != 1: print('FAIL chirp globe', c.count(start), c.count(end)); sys.exit(1)
i = c.index(start); j = c.index(end) + len(end)
assert j > i and j - i < 1500
c = c[:i] + "f&&(0,L.jsx)(`span`,{className:`pp-chirp-globe`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppIco(`PNGLOBE`)}})" + c[j:]
print('OK: chirp globe')
css = "body .pp-chirp-globe{display:inline-flex;width:14px;height:14px;flex-shrink:0;color:#0a0a0a}body .pp-chirp-globe svg{width:14px;height:14px;stroke-width:2.4}"
k = c.index("body .lb-ic{"); c = c[:k] + css + c[k:]
print('OK: css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
