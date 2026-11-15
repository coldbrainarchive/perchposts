#!/usr/bin/env python3
"""Patch v1073 -> v1074: the box around the bird, name and level pill on profile cards matches the Hatched / Clan / Worms
rows (card colour, faint tint, thin border) instead of the level colour; the level pill already carries that colour."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1073.js'
dst = '_deploy/assets/index-DUcNPOLc-v1074.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('rc:_rk?_rk.c||`#c084fc`:null,rtop:!!_rk&&_rk.n===`Legendary Brood`,title:_un,sub:_rk?',
      'rc:_resolvedCol||`#c084fc`,rtop:!1,title:_un,sub:_rk?', 'box uses the card colour')
c += r''';(()=>{try{const s=document.createElement(`style`);s.textContent=`
.bc-card:not(.bc-nest) .bc-head.bc-rbox{border:1px solid color-mix(in srgb,var(--rc) 16%,transparent);background:color-mix(in srgb,var(--rc) 6%,#15171d);box-shadow:none;border-radius:16px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
