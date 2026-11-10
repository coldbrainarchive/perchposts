#!/usr/bin/env python3
"""Patch v952 -> v953: the post page preview notes hidden pins ("📌 +2 more pinned") under its 3 pins."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v952.js'
dst = '_deploy/assets/index-DUcNPOLc-v953.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('let _nl=0,_np=0,_df=', 'let _nl=0,_np=0,_pmo=0,_df=', 'count var')
patch('if(_pv){let _ps=_rev.filter(_x=>_x.pinned).slice(0,3),', 'if(_pv){_pmo=_rev.filter(_x=>_x.pinned).length-3;let _ps=_rev.filter(_x=>_x.pinned).slice(0,3),', 'count pins')
patch('_rev.forEach((_e,_i)=>{_out.push(_R(',
      '_rev.forEach((_e,_i)=>{if(_pv&&_pmo>0&&_i===_nl)_out.push((0,L.jsx)(`div`,{className:`pin-more-note`,children:`📌 +${_pmo} more pinned`},`pmn`));_out.push(_R(',
      'note under pins')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.pin-more-note{align-self:center;flex-shrink:0;margin:2px auto 6px;height:24px;line-height:22px;padding:0 11px;border-radius:999px;border:1px solid rgba(148,163,184,.18);background:rgba(148,163,184,.06);color:#94a3b8;font-size:11px;font-weight:700;box-sizing:border-box;white-space:nowrap}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
