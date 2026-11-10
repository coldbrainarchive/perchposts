#!/usr/bin/env python3
"""Patch v987 -> v988: the chirp preview filter pill sits in the right-hand corner of the preview header,
opposite the 💬 count in the left; its menu opens right-aligned under it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v987.js'
dst = '_deploy/assets/index-DUcNPOLc-v988.js'
c = open(src, encoding='utf-8').read()
old = 'm.style.left=Math.max(8,Math.min(r.left,innerWidth-m.offsetWidth-8))+`px`;'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, 'm.style.left=Math.max(8,Math.min(r.right-m.offsetWidth,innerWidth-m.offsetWidth-8))+`px`;')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.comments-shell.chat-preview .chat-panel-header>div:first-child{display:flex;align-items:center}.cp-filter{margin-left:auto!important}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
