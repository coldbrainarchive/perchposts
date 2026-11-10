#!/usr/bin/env python3
"""Patch v945 -> v946: no REACTIONS label; the open chirp menu just shows the reacted birds' pills."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v945.js'
dst = '_deploy/assets/index-DUcNPOLc-v946.js'
c = open(src, encoding='utf-8').read()
old = 'children:[(0,L.jsx)(`div`,{className:`rx-who-lb`,children:`Reactions`}),...rows.map('
if c.count(old) != 1: print('FAIL label', c.count(old)); sys.exit(1)
c = c.replace(old, 'children:[...rows.map(')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.rx-who{padding-top:6px}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
