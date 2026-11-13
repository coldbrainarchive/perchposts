#!/usr/bin/env python3
"""Patch v1038 -> v1039: pictures in the full-screen link view are always a 16:9 news-card shape, so tall (portrait)
photos no longer take over the screen. They're cropped toward the top so faces stay in frame."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1038.js'
dst = '_deploy/assets/index-DUcNPOLc-v1039.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel .reel-img{aspect-ratio:16/9;height:auto;object-fit:cover;object-position:50% 25%}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
