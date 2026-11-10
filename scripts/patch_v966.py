#!/usr/bin/env python3
"""Patch v965 -> v966: pinned chirps keep their glow in the react view. The copy's frame no longer clips
(the glow ring was being cut into square corners) and the drop shadow only applies to unpinned chirps;
there's room around the copy for the glow."""
src = '_deploy/assets/index-DUcNPOLc-v965.js'
dst = '_deploy/assets/index-DUcNPOLc-v966.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.ri-top{padding:28px 22px 26px}
.ri-chirp{overflow:visible}
.ri-chirp>.chat-msg-body:not(.chat-pinned){box-shadow:0 10px 34px rgba(0,0,0,.55)}
.ri-chirp>.chat-msg-body.chat-pinned{box-shadow:0 0 0 4px rgba(var(--gc,192,132,252),.6),0 0 20px rgba(var(--gc,192,132,252),.8),0 10px 34px rgba(0,0,0,.5)}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
