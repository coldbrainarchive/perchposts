#!/usr/bin/env python3
"""Patch v1051 -> v1052: after the first swipe the top hint keeps a "Tap to close" line under the ⌃ arrow
(previously only the arrow stayed)."""
src = '_deploy/assets/index-DUcNPOLc-v1051.js'
dst = '_deploy/assets/index-DUcNPOLc-v1052.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel .reel-hint.small:not(.end){flex-direction:column;gap:1px}
.reel .reel-hint.small:not(.end)::after{content:"Tap to close"}
.reel .reel-hint.small:not(.end) .reel-arrow{line-height:1}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
