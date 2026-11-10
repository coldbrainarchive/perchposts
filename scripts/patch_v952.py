#!/usr/bin/env python3
"""Patch v951 -> v952: the full chat shows every pinned chirp (no cap, no "N more pinned" pill);
the post page preview shows at most the 3 newest pins."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v951.js'
dst = '_deploy/assets/index-DUcNPOLc-v952.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('if(_ex>0)_out.push((0,L.jsx)(`button`,{type:`button`,className:`pin-more`', 'if(!1)_out.push((0,L.jsx)(`button`,{type:`button`,className:`pin-more`', 'chat: no pill')
patch('_out.push(_R(_p2[k],!0,`pc-`+_p2[k].id,k>=3,_solo.has(_p2[k].id)));', '_out.push(_R(_p2[k],!0,`pc-`+_p2[k].id,!1,_solo.has(_p2[k].id)));', 'chat: all pins shown')
patch('if(_pv){let _ps=_rev.filter(_x=>_x.pinned),', 'if(_pv){let _ps=_rev.filter(_x=>_x.pinned).slice(0,3),', 'preview: 3 pins')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
