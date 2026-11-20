#!/usr/bin/env python3
"""Patch v1282 -> v1283: the Notifications chevron always shows (also on the Your Nest tab and with an empty list),
so it doesn't come and go. It only flips up while the clear bar is open."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1282.js'
dst = '_deploy/assets/index-DUcNPOLc-v1283.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("children:e.id===`notifications`&&c===e.id&&j.length>0?(0,L.jsxs)(`span`,{className:`n-tabw`,children:[e.label,(0,L.jsx)(`span`,{className:`n-chev`+(_showClear?` up`:``)",
      "children:e.id===`notifications`?(0,L.jsxs)(`span`,{className:`n-tabw`,children:[e.label,(0,L.jsx)(`span`,{className:`n-chev`+(_showClear&&c===e.id&&j.length>0?` up`:``)", 'always show')
patch("body .n-chev{display:inline-flex;width:13px;height:13px;color:#94a3b8;", "body .n-chev{display:inline-flex;width:13px;height:13px;color:currentColor;opacity:.75;", 'follow tab colour')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
