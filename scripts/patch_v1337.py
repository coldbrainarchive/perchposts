#!/usr/bin/env python3
"""Patch v1336 -> v1337: post scroller top row: the time pill ("24m ago") no longer overlaps the tags.
The space kept free for it at the top right was a fixed 50px; now it's measured from the pill itself
(fallback 76px), on the slide and on the copied info panel."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1336.js'
dst = '_deploy/assets/index-DUcNPOLc-v1337.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("body .reel-head.has-who{position:relative;flex-wrap:wrap;gap:6px;padding-right:50px}",
      "body .reel-head.has-who{position:relative;flex-wrap:wrap;gap:6px;padding-right:var(--rtw,76px)}", 'slide head')
patch("body .reel-pinfo-in .reel-head{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px;position:relative;padding-right:50px}",
      "body .reel-pinfo-in .reel-head{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px;position:relative;padding-right:var(--rtw,76px)}", 'panel head')
c += r"""
;(()=>{try{let q=0;const fit=()=>{q=0;document.querySelectorAll(`.reel-head`).forEach(h=>{const t=h.querySelector(`:scope>.reel-time`);if(!t)return;const w=t.offsetWidth;if(!w)return;const v=(w+8)+`px`;if(h.style.getPropertyValue(`--rtw`)!==v)h.style.setProperty(`--rtw`,v)})};
 new MutationObserver(()=>{if(!q)q=requestAnimationFrame(fit)}).observe(document.body,{childList:!0,subtree:!0});addEventListener(`resize`,()=>{if(!q)q=requestAnimationFrame(fit)})}catch(e){}})();
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
