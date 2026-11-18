#!/usr/bin/env python3
"""Patch v1199 -> v1200 (scroller):
- Photo sets: the "1 / 5" counter is a pill the same size and style as the ✕, level with it at the top right.
- Media slides: the gap from the name/tags row to the title matches the gap from the title to VIEW POST ↗."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1199.js'
dst = '_deploy/assets/index-DUcNPOLc-v1200.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
css = ("body .reel .reel-m .reel-count{position:absolute!important;top:calc(10px + env(safe-area-inset-top))!important;right:12px!important;left:auto!important;height:38px;min-width:38px;box-sizing:border-box;padding:0 14px!important;display:flex;align-items:center;justify-content:center;border-radius:999px!important;background:rgba(0,0,0,.45)!important;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);color:#fff!important;font-size:14px!important;font-weight:700!important;line-height:1;z-index:4}"
       "body .reel .reel-m .reel-head{margin-bottom:8px!important}"
       "body .reel .reel-m .reel-title{line-height:1.2!important}"
       "body .reel .reel-m a.reel-site{margin-top:8px!important;padding:0!important;line-height:1!important}")
patch("ct.className=`reel-count`;ct.textContent=`1 / ${d.n}`;med.appendChild(ct)", "ct.className=`reel-count`;ct.textContent=`1 / ${d.n}`;s.appendChild(ct)", 'counter above the fade')
patch("const ct=med.querySelector(`.reel-count`);if(ct)ct.textContent=`${k+1} / ${N}`", "const ct=s.querySelector(`.reel-count`);if(ct)ct.textContent=`${k+1} / ${N}`", 'counter lookup')
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
