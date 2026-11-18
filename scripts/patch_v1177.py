#!/usr/bin/env python3
"""Patch v1176 -> v1177: the post card's Share pill is a round arrow-only button again
(it briefly widens to show "Copied" / "Shared")."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1176.js'
dst = '_deploy/assets/index-DUcNPOLc-v1177.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:h,children:[(0,L.jsx)(`span`,{className:`pp-ic pp-share`,dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),(0,L.jsx)(`span`,{children:o})]}),",
      "(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill pc-share`+(o!==`Share`?` pc-said`:``),\"aria-label\":`Share`,onClick:h,children:[(0,L.jsx)(`span`,{className:`pp-ic pp-share`,dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),o!==`Share`?(0,L.jsx)(`span`,{children:o}):null]}),",
      'card share: arrow only')
patch("body .lb-ic{", "body .feed-post-actions .pc-share{width:34px;padding:0!important;justify-content:center}body .feed-post-actions .pc-share.pc-said{width:auto;padding:0 12px!important}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
