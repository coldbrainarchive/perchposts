#!/usr/bin/env python3
"""Patch v1177 -> v1178: everywhere (cards, post page, search / tag pickers, new-post picker), the board / country / region tags are outlined (usernames stay solid) like the
link-preview reel's tags (coloured outline + coloured text, no solid fill) instead of solid blocks of colour."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1177.js'
dst = '_deploy/assets/index-DUcNPOLc-v1178.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# each pill carries its colour in --pc
patch("return(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:n?4:6,height:n?22:26,padding:n?`0 7px`:`0 8px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,background:`#cbd5e1`,",
      "return(0,L.jsxs)(`span`,{className:`pp-tag`,style:{\"--pc\":`#cbd5e1`,display:`inline-flex`,alignItems:`center`,gap:n?4:6,height:n?22:26,padding:n?`0 7px`:`0 8px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,background:`#cbd5e1`,", 'country pill colour')
patch("return(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:t?4:6,height:t?22:26,padding:t?`0 7px`:`0 8px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,background:_bc,",
      "return(0,L.jsxs)(`span`,{className:`pp-tag`,style:{\"--pc\":_bc,display:`inline-flex`,alignItems:`center`,gap:t?4:6,height:t?22:26,padding:t?`0 7px`:`0 8px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,background:_bc,", 'board pill colour')
patch("return(0,L.jsxs)(`span`,{className:`user-pill`,style:{color:N?`#ffffff`:`#0a0a0a`,",
      "return(0,L.jsxs)(`span`,{className:`user-pill`,style:{\"--pc\":o?`#ffffff`:s?`#c084fc`:N?`#ef4444`:c,color:N?`#ffffff`:`#0a0a0a`,", 'user pill colour')
sel = lambda x: ",".join(f"body {s}" for s in x)
P = [".pp-tag"]
css = (sel(P) + "{background:transparent!important;color:var(--pc)!important;border:1.5px solid var(--pc)!important;box-sizing:border-box}"
       )
patch("body .lb-ic{", css + "body .lb-ic{", 'outlined tags')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
