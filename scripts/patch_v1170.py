#!/usr/bin/env python3
"""Patch v1169 -> v1170: on huddles, the pinned / locked / archived icons sit in the title row (before the age pill)
instead of floating in the top-right corner over it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1169.js'
dst = '_deploy/assets/index-DUcNPOLc-v1170.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

B = "(c.pinned||c.locked||c.frozen)&&(0,L.jsxs)(`div`,{className:`post-badges`,style:{position:`absolute`,top:14,right:16,display:`flex`,gap:4,alignItems:`center`},children:[c.pinned&&(0,L.jsx)(`span`,{className:`post-badge pp-badge-ic`,title:`Pinned`,dangerouslySetInnerHTML:{__html:_ppIco(`PIN`)}}),c.locked&&(0,L.jsx)(`span`,{className:`post-badge pp-badge-ic`,title:`Locked`,dangerouslySetInnerHTML:{__html:_ppIco(`LOCK`)}}),c.frozen&&(0,L.jsx)(`span`,{title:`Archived`,className:`post-badge pp-badge-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`ARCHIVE`)}})]})"
i = c.index("className:c.is_huddle?`content-card feed-post-card hp-card`")
j = c.index(B, i)
if j - i > 4000: print('FAIL badges not near'); sys.exit(1)
c = c[:j] + "!c.is_huddle&&" + c[j:]; print('OK: no floating badges on huddles')
inline = B.replace("(c.pinned||c.locked||c.frozen)&&", "(c.pinned||c.locked||c.frozen)?").replace(
    "style:{position:`absolute`,top:14,right:16,display:`flex`,gap:4,alignItems:`center`}", "className:`post-badges hp-badges`,key:`b`").replace("className:`post-badges`,", "") + ":null"
patch("children:c.is_huddle?[(0,L.jsx)(`span`,{className:`hp-tt`,children:c.title},`t`),",
      "children:c.is_huddle?[(0,L.jsx)(`span`,{className:`hp-tt`,children:c.title},`t`)," + inline + ",", 'badges in the title row')
patch("body .lb-ic{", "body .hp-badges{display:flex;gap:4px;align-items:center;flex-shrink:0}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
