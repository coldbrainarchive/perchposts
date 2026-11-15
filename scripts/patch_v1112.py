#!/usr/bin/env python3
"""Patch v1111 -> v1112: the huddle owner's crown is our own crown icon in the site purple, centred on top of the
owner's bubble (was the 👑 emoji at the top-right corner). The "Owner" tags in the members list use it too."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1111.js'
dst = '_deploy/assets/index-DUcNPOLc-v1112.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("m.owner?(0,L.jsx)(`span`,{className:`hx-crown`,children:`👑`}):null",
      "m.owner?(0,L.jsx)(`span`,{className:`hx-crown pp-ic`,title:`Owner`,dangerouslySetInnerHTML:{__html:_ppIco(`CROWN`)}}):null", 'crown on the bubble')
patch("m.owner?(0,L.jsx)(`span`,{className:`hx-tag`,children:`👑 Owner`}):null",
      "m.owner?(0,L.jsx)(`span`,{className:`hx-tag`,children:_ppLbl(`👑 Owner`)}):null", 'owner tag 1')
patch("m.owner?(0,L.jsx)(`span`,{className:`hx-tag`,children:`👑 Owner`},`o`):null",
      "m.owner?(0,L.jsx)(`span`,{className:`hx-tag`,children:_ppLbl(`👑 Owner`)},`o`):null", 'owner tag 2')
patch('const _PPE={"📌":`PIN`,', 'const _PPE={"👑":`CROWN`,"📌":`PIN`,', 'crown label icon')
css = ("body .hx-crown{top:-11px;left:50%;right:auto;transform:translateX(-50%);font-size:0;color:#c084fc;"
       "filter:drop-shadow(0 0 1px #15171d) drop-shadow(0 0 1px #15171d) drop-shadow(0 1px 1px rgba(0,0,0,.5))}"
       "body .hx-crown .ri{width:14px;height:14px;stroke-width:2.5;display:block;fill:rgba(192,132,252,.35)}"
       "body .hx-tag .lb-ic .ri{color:#c084fc}")
patch("body .lb-ic{", css + "body .lb-ic{", 'crown styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
