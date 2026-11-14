#!/usr/bin/env python3
"""Patch v1056 -> v1057: level pill on profile cards a bit smaller again (19px tall, 9px text, 10.5px emoji)."""
src = '_deploy/assets/index-DUcNPOLc-v1056.js'
dst = '_deploy/assets/index-DUcNPOLc-v1057.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.bc-rank.bc-rank-sm{height:19px;gap:4px;padding:0 7px 0 6px;border-width:1.25px;font-size:9px;letter-spacing:.06em}
.bc-rank-sm .bc-re{font-size:10.5px}
.bc-id:has(.bc-rank-sm){gap:6px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
