#!/usr/bin/env python3
"""Patch v1281 -> v1282: a small chevron next to "Notifications" (when that tab is open and has notifications)
shows that tapping it opens the Mark all read / Clear all bar; it flips up while the bar is open."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1281.js'
dst = '_deploy/assets/index-DUcNPOLc-v1282.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
CH = '<svg viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2.6\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\"><path d=\\"M6 9l6 6 6-6\\"/></svg>'
patch("fontWeight:c===e.id?700:500,fontSize:13,cursor:`pointer`},children:e.label},e.id))",
      "fontWeight:c===e.id?700:500,fontSize:13,cursor:`pointer`},\"aria-expanded\":e.id===`notifications`&&c===e.id&&j.length>0?!!_showClear:void 0,children:e.id===`notifications`&&c===e.id&&j.length>0?(0,L.jsxs)(`span`,{className:`n-tabw`,children:[e.label,(0,L.jsx)(`span`,{className:`n-chev`+(_showClear?` up`:``),dangerouslySetInnerHTML:{__html:\"" + CH + "\"}})]}):e.label},e.id))", 'chevron')
patch("body .lb-ic{", "body .n-tabw{display:inline-flex;align-items:center;gap:4px}body .n-chev{display:inline-flex;width:13px;height:13px;color:#94a3b8;transition:transform .18s}body .n-chev svg{width:100%;height:100%}body .n-chev.up{transform:rotate(180deg)}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
