#!/usr/bin/env python3
"""Patch v1360 -> v1361: tidier post chat header — the tiny ▾ is replaced by a proper chevron button at the right
end of the top row (flips when the post is open); title and bird/site line sit closer together."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1360.js'
dst = '_deploy/assets/index-DUcNPOLc-v1361.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch(",(0,L.jsx)(`span`,{className:`cv`+(open?` up`:``),children:`▾`})", "", 'drop tiny triangle')
patch("(0,L.jsx)(_ChHeadTx,{post:c,title:_ct,n:_cn,open:_chx},`chtx`)",
      "[(0,L.jsx)(_ChHeadTx,{post:c,title:_ct,n:_cn,open:_chx},`chtx`),(0,L.jsx)(`span`,{className:`ch-cv`+(_chx?` up`:``),\"aria-hidden\":`true`,dangerouslySetInnerHTML:{__html:`<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.4\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6 9.5l6 6 6-6\"/></svg>`}},`chcv`)]", 'chevron button')
patch("body .lb-ic{",
 "body .ch-tx{gap:3px;flex:1;min-width:0}body .ch-t{line-height:1.2}body .ch-m{line-height:1.2}"
 "body .ch-cv{margin-left:auto;flex-shrink:0;width:32px;height:32px;border-radius:999px;border:1px solid #2e303a;background:#1d2029;color:#c084fc;display:inline-flex;align-items:center;justify-content:center;transition:transform .2s,background .2s}"
 "body .ch-cv svg{width:17px;height:17px}body .ch-cv.up{transform:rotate(180deg);background:#c084fc22;border-color:#c084fc66}"
 "body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
