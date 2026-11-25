#!/usr/bin/env python3
"""Patch v1377 -> v1378: the post card shared into a huddle chat shows the share count beside flaps and chirps."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1377.js'
dst = '_deploy/assets/index-DUcNPOLc-v1378.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("(0,L.jsxs)(`span`,{children:[(0,L.jsx)(`span`,{dangerouslySetInnerHTML:{__html:_ppIco(`CHAT`)}}),d.chirps]}),d.chirps>0?",
      "(0,L.jsxs)(`span`,{children:[(0,L.jsx)(`span`,{dangerouslySetInnerHTML:{__html:_ppIco(`CHAT`)}}),d.chirps]}),(0,L.jsxs)(`span`,{className:`psc-sh`,children:[(0,L.jsx)(`span`,{dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),d.shares||0]}),d.chirps>0?", 'share count on card')
patch("body .lb-ic{", "body .psc-c .psc-sh svg{width:10px;height:10px}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
