#!/usr/bin/env python3
"""Patch v1089 -> v1090: on the profile card, the level moves out from under the name into its own row at the top
of the list (above Hatched). The row's outline and the level name are in the level's colour.
Card rows can now take a 4th item: extra style for that row."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1089.js'
dst = '_deploy/assets/index-DUcNPOLc-v1090.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("stats.filter(Boolean).map(([e,l,v])=>(0,L.jsxs)(`div`,{className:`bc-row`,style:{background:mx(6,`#15171d`),border:`1px solid ${mx(16)}`}",
      "stats.filter(Boolean).map(([e,l,v,o])=>(0,L.jsxs)(`div`,{className:`bc-row`,style:{background:mx(6,`#15171d`),border:`1px solid ${mx(16)}`,...(o||{})}",
      'rows take extra style')
patch("rtop:!1,title:_un,sub:_rk?(0,L.jsxs)(`span`,{className:`bc-rank bc-rank-sm`+(_rk.n===`Legendary Brood`?` bc-rank-top`:``),style:{\"--rc\":_rk.c||`#c084fc`},children:[(0,L.jsx)(`span`,{className:`bc-re`,children:_rk.e}),_rk.n]}):null,"
      "stats:[[`🥚`,`Hatched`,_hd],",
      "rtop:!1,title:_un,sub:null,"
      "stats:[_rk?[_rk.e,`Level`,(0,L.jsx)(`span`,{style:{color:_rk.c||`#c084fc`},children:_rk.n}),{border:`1.5px solid ${_rk.c||`#c084fc`}`}]:null,[`🥚`,`Hatched`,_hd],",
      'level row above Hatched')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
