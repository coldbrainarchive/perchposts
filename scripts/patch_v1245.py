#!/usr/bin/env python3
"""Patch v1244 -> v1245: mod panel → Flock: each bird's row shows their flaps (purple flap icon + count, same number
as on their bird card), after their worms."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1244.js'
dst = '_deploy/assets/index-DUcNPOLc-v1245.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("return _wr?` · ${_wr.e} ${_wr.n} · 🪱 ${_wc}`:``;})(),",
      "return _wr?` · ${_wr.e} ${_wr.n} · 🪱 ${_wc}`:``;})(),` · `,(0,L.jsxs)(`span`,{className:`fl-flaps`,title:`Flaps`,children:[(0,L.jsx)(`span`,{className:`pp-ic fl-flap`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),n.flaps||0]}),",
      'flaps in the Flock row')
patch("body .lb-ic{", "body .fl-flaps{white-space:nowrap}body .fl-flap{display:inline-block;width:13px;height:13px;vertical-align:-2px;margin-right:3px;color:#c084fc}body .fl-flap svg{width:100%;height:100%;display:block}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
