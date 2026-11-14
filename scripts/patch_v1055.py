#!/usr/bin/env python3
"""Patch v1054 -> v1055:
- Your Nest: the circle behind the level emoji takes the level colour (same as the box around it).
- Profile cards (looking up other people): the level becomes a pill in the level colour, with the level emoji inside,
  under the username. The small level badge on the avatar is dropped since the pill now shows it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1054.js'
dst = '_deploy/assets/index-DUcNPOLc-v1055.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('badge:_rk?_rk.e:`🐣`,title:_un,sub:_rk?_rk.n:null,',
      'title:_un,sub:_rk?(0,L.jsxs)(`span`,{className:`bc-rank bc-rank-sm`+(_rk.n===`Legendary Brood`?` bc-rank-top`:``),style:{"--rc":_rk.c||`#c084fc`},children:[(0,L.jsx)(`span`,{className:`bc-re`,children:_rk.e}),_rk.n]}):null,',
      'profile rank pill')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.bc-rbox .bc-av{background:color-mix(in srgb,var(--rc) 22%,#1b1d24)!important;border:1.5px solid color-mix(in srgb,var(--rc) 75%,transparent)!important}
.bc-sub:has(.bc-rank){display:flex}
.bc-rank-sm{height:26px;gap:6px;padding:0 11px 0 8px;font-size:11.5px}
.bc-rank-sm .bc-re{font-size:15px;line-height:1;letter-spacing:0}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
