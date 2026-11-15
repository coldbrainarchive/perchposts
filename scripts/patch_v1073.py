#!/usr/bin/env python3
"""Patch v1072 -> v1073:
- Your Nest: bigger level emoji (36px -> 50px).
- Profile cards: the bird, username and level pill sit in a box in the level's colour, like the Your Nest box.
  The username keeps the person's own colour (only Your Nest colours its title with the level)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1072.js'
dst = '_deploy/assets/index-DUcNPOLc-v1073.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('face:(0,L.jsx)(`span`,{style:{fontSize:36,lineHeight:1},children:_rank.e})',
      'face:(0,L.jsx)(`span`,{style:{fontSize:50,lineHeight:1},children:_rank.e})', 'bigger nest emoji')
patch('title:_un,sub:_rk?', 'rc:_rk?_rk.c||`#c084fc`:null,rtop:!!_rk&&_rk.n===`Legendary Brood`,title:_un,sub:_rk?', 'profile card level box')
patch('.bc-rbox .bc-name{color:var(--rc)!important}', '.bc-nest .bc-rbox .bc-name{color:var(--rc)!important}', 'level-coloured title only in the nest')
c += r''';(()=>{try{const s=document.createElement(`style`);s.textContent=`
.bc-nest .bc-rbox .bc-av{width:64px;height:64px}
.bc-card:not(.bc-nest) .bc-rbox{padding:12px 14px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
