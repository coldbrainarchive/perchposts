#!/usr/bin/env python3
"""Patch v1304 -> v1305: our worm icon on Bird ID cards, the nest card and the Flock list (were 🪱); the line worm is
~15% smaller everywhere."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1304.js'
dst = '_deploy/assets/index-DUcNPOLc-v1305.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
W = "(0,L.jsx)(`span`,{className:`pp-ic bc-flap bc-worm`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}})"
patch("[`🪱`,`Worms`,_wc]", "[" + W + ",`Worms`,_wc]", 'Bird ID + nest rows', 2)
patch("return _wr?` · ${_wr.e} ${_wr.n} · 🪱 ${_wc}`:``;",
      "return _wr?[` · ${_wr.e} ${_wr.n} · `,(0,L.jsx)(`span`,{className:`pp-ic fl-worm`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}},`w`),` ${_wc}`]:``;", 'Flock row')
patch("body .lb-ic{", "body .ri.wline{transform:scale(.85);transform-origin:center}body .fl-worm{display:inline-flex;vertical-align:-2px}body .fl-worm .ri{width:13px;height:13px}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
