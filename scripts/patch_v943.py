#!/usr/bin/env python3
"""Patch v942 -> v943: the Reactions list in an open chirp menu is smaller, about the size of the chirp's
username header (24px rows, 12px bird, 12px name). The long-press sheet keeps its bigger rows."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v942.js'
dst = '_deploy/assets/index-DUcNPOLc-v943.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('function _rxRow(r,i){const f=_rxFace(r.name,16)', 'function _rxRow(r,i,_a,sm){const f=_rxFace(r.name,sm?12:16)', 'row size param')
patch('children:`Reactions`}),...rows.map(_rxRow)]})', 'children:`Reactions`}),...rows.map((r,i)=>_rxRow(r,i,0,1))]})', 'menu rows small')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.rx-who{gap:4px;padding:2px 12px 10px}
.rx-who .rx-row{min-height:24px;height:24px;gap:6px;padding:0 9px 0 2px}
.rx-who .rx-av{width:20px;height:20px}
.rx-who .rx-nm{font-size:12px}
.rx-who .rx-qs{font-size:13px;letter-spacing:1px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
