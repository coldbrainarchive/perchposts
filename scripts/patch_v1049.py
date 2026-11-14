#!/usr/bin/env python3
"""Patch v1048 -> v1049: the fixed action bar in the full-screen link view drops the glass look and becomes three
separate outline pills styled like the tag/time pills at the top of the preview (thin grey outline, small bold text,
dark see-through fill). Flapped = purple outline + text. Still fixed while posts swipe underneath."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1048.js'
dst = '_deploy/assets/index-DUcNPOLc-v1049.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel .reel-dock{height:32px;padding:0;gap:8px;overflow:visible;background:transparent;border:0;box-shadow:none;-webkit-backdrop-filter:none;backdrop-filter:none;border-radius:0}
.reel .reel-dock::before{display:none}
.reel .reel-dock .reel-dbtn{box-sizing:border-box;height:32px;gap:6px;border:1.5px solid #94a3b8;border-radius:999px;color:#cbd5e1;background:rgba(11,12,16,.62);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);font-size:12px;font-weight:800;letter-spacing:.02em}
.reel .reel-dock .reel-dbtn + .reel-dbtn::before{display:none}
.reel .reel-dock .reel-dbtn:active{background:rgba(148,163,184,.18)}
.reel .reel-dock .reel-dbtn.reel-flap .ri{width:18px;height:18px}
.reel .reel-dock .reel-dbtn.reel-chat .ri{width:14px;height:14px}
.reel .reel-dock .reel-dbtn.reel-share .ri{width:10px;height:10px}
.reel .reel-dock .reel-dbtn.reel-share{gap:5px}
.reel .reel-dock .reel-dbtn.on{color:#c084fc;border-color:#c084fc;background:rgba(11,12,16,.62)}
.reel .reel-dock .reel-dbtn.on:active{background:rgba(192,132,252,.16)}
.reel .reel-dock .reel-dbtn.on .ri{filter:none}
.reel .reel-dock .reel-dbtn.on .n{color:#c084fc}
.reel .reel-dock .reel-dbtn.done{color:#c084fc;border-color:#c084fc}
.reel .reel-slide{padding-bottom:calc(86px + env(safe-area-inset-bottom))}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
