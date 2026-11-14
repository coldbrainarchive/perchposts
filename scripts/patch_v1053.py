#!/usr/bin/env python3
"""Patch v1052 -> v1053: in Your Nest, the level name sits in an outline pill (like the tag pills) coloured by level.
Each rank in _RANKS gets a colour `c`, running warm -> cool -> gold as you level up."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1052.js'
dst = '_deploy/assets/index-DUcNPOLc-v1053.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
cols = {'Endangered':'#f87171','Hatchling':'#fde68a','Nestling':'#facc15','Fledgling':'#fb923c','Forager':'#a3e635',
 'Bird of Prey':'#4ade80','Mixed-Flock Attendant':'#2dd4bf','Seasoned Migrant':'#38bdf8','Continental Migrant':'#60a5fa',
 'Peak Plumage':'#a78bfa','Master Layer':'#e879f9','Legendary Brood':'#fbbf24'}
for n, col in cols.items():
    patch('n:`%s`,d:' % n, 'n:`%s`,c:`%s`,d:' % (n, col), 'colour ' + n)
patch('title:_rank.n,desc:_rank.d',
      'title:(0,L.jsx)(`span`,{className:`bc-rank`+(_rank.n===`Legendary Brood`?` bc-rank-top`:``),style:{"--rc":_rank.c||`#c084fc`},children:_rank.n}),desc:_rank.d',
      'nest rank pill')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.bc-nest .bc-nt{overflow:visible;white-space:normal}
.bc-rank{display:inline-flex;align-items:center;height:26px;padding:0 12px;border-radius:999px;border:1.5px solid var(--rc);color:var(--rc);background:color-mix(in srgb,var(--rc) 14%,transparent);font-size:12px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;white-space:nowrap;line-height:1;box-sizing:border-box}
.bc-rank-top{box-shadow:0 0 12px color-mix(in srgb,var(--rc) 45%,transparent)}
.bc-nest .bc-id{gap:7px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
