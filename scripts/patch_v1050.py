#!/usr/bin/env python3
"""Patch v1049 -> v1050: the fixed action bar goes back to one bar, but styled like the top tag/time pills:
one rounded outline (1.5px grey), dark see-through fill, small bold text, thin dividers between the three buttons.
Flapped = purple icon + number."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1049.js'
dst = '_deploy/assets/index-DUcNPOLc-v1050.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel .reel-dock{height:34px;padding:0;gap:0;overflow:hidden;box-sizing:border-box;border:1.5px solid #94a3b8;border-radius:999px;background:rgba(11,12,16,.62);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);box-shadow:none}
.reel .reel-dock .reel-dbtn{height:100%;border:0;border-radius:0;background:transparent;-webkit-backdrop-filter:none;backdrop-filter:none}
.reel .reel-dock .reel-dbtn + .reel-dbtn::before{display:block;content:"";position:absolute;left:0;top:9px;bottom:9px;width:1.5px;background:rgba(148,163,184,.45)}
.reel .reel-dock .reel-dbtn:active{background:rgba(148,163,184,.18)}
.reel .reel-dock .reel-dbtn.on,.reel .reel-dock .reel-dbtn.done{border:0;background:transparent}
.reel .reel-dock .reel-dbtn.on:active{background:rgba(192,132,252,.16)}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
