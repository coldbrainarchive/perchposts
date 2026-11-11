#!/usr/bin/env python3
"""Patch v1008 -> v1009: the New Post body / opening message box uses 16px text so iPhone Safari doesn't zoom in
when you tap it (Safari zooms on any text box under 16px)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1008.js'
dst = '_deploy/assets/index-DUcNPOLc-v1009.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.nh-card .nh-msg{font-size:16px!important}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
