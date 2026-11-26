#!/usr/bin/env python3
"""Patch v1395 -> v1396: Take flight notifications.
- The GLOBE badge on a notification shows the globe line icon (it printed the word "GLOBE").
- A notification with a link to the globe page (/globe/...) opens it as a normal page load: the globe isn't part of
  this app, so the in-app router can't show it (Take flight's "still in the water" / "drowned" notices link to
  /globe/?go=me, which flies down to your bird)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1395.js'
dst = '_deploy/assets/index-DUcNPOLc-v1396.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch("e.icon===`🪱`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}):e.icon}):null]});",
      "e.icon===`🪱`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}):e.icon===`GLOBE`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#60a5fa`},dangerouslySetInnerHTML:{__html:_ppIco(`GLOBE`)}}):e.icon}):null]});",
      'globe badge')
patch("onClick:_ev=>{if(e.req&&e.req.kind===`invite`&&e.req.status!==`accepted`){_ev.preventDefault();_nMark(e);return}",
      "onClick:_ev=>{if(e.link&&/^\\/globe\\//.test(e.link)){_ev.preventDefault();_nMark(e);location.href=e.link;return}if(e.req&&e.req.kind===`invite`&&e.req.status!==`accepted`){_ev.preventDefault();_nMark(e);return}",
      'globe links open the globe page')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
