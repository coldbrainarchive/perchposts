#!/usr/bin/env python3
"""Patch v1018 -> v1019: no see-through to the page behind a full-screen chat when the keyboard is open.
With the keyboard up the chat shrinks to the space above it; iPhone's see-through keyboard and its glass bar
showed the page underneath (e.g. the flock feed). A solid dark backdrop now sits behind any open full-screen chat
(just under it, above everything else on the page), reaching past the screen edges."""
src = '_deploy/assets/index-DUcNPOLc-v1018.js'
dst = '_deploy/assets/index-DUcNPOLc-v1019.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
html.chat-open body::after{content:"";position:fixed;left:0;right:0;top:-50vh;bottom:-50vh;background:#14161c;z-index:44;pointer-events:none}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
