#!/usr/bin/env python3
"""Patch v1050 -> v1051: the "Swipe up for the next post · Tap to close" line moves to the top of the full-screen
link view, replacing the separate "Tap to close" line there. The bar drops a little lower now the bottom is free."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1050.js'
dst = '_deploy/assets/index-DUcNPOLc-v1051.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel .reel-top{display:none}
.reel .reel-hint{top:calc(14px + env(safe-area-inset-top));bottom:auto}
.reel .reel-dock{bottom:calc(22px + env(safe-area-inset-bottom))}
.reel .reel-slide{padding-bottom:calc(72px + env(safe-area-inset-bottom))}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
