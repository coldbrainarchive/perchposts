#!/usr/bin/env python3
"""Patch v1055 -> v1056: the level pill on profile cards is smaller and lighter, sized like the tag pills on posts
(22px tall, small caps text, small emoji), with a bit more space under the username so the pair sits centred
beside the picture."""
src = '_deploy/assets/index-DUcNPOLc-v1055.js'
dst = '_deploy/assets/index-DUcNPOLc-v1056.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.bc-id:has(.bc-rank-sm){gap:7px}
.bc-sub:has(.bc-rank-sm){line-height:1}
.bc-rank.bc-rank-sm{height:22px;gap:5px;padding:0 9px 0 7px;border-width:1.5px;font-size:10px;font-weight:800;letter-spacing:.06em;background:color-mix(in srgb,var(--rc) 10%,transparent)}
.bc-rank-sm .bc-re{font-size:12px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
