#!/usr/bin/env python3
"""Patch v1297 -> v1298: Share sheet + keyboard: no see-through gap.
The backdrop stays full screen; the sheet's own background reaches down behind iOS's form bar and the keyboard
(bottom padding = keyboard height), so its contents sit just above the keyboard and nothing shows between."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1297.js'
dst = '_deploy/assets/index-DUcNPOLc-v1298.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const fit=()=>{const o=ovR.current;if(!o)return;o.style.top=vv.offsetTop+`px`;o.style.height=vv.height+`px`;o.style.bottom=`auto`};",
      "const fit=()=>{const o=ovR.current,sh=o&&o.querySelector(`.ps-sheet`);if(!sh)return;const kb=Math.max(0,Math.round(innerHeight-vv.height-vv.offsetTop));sh.style.paddingBottom=kb>40?`calc(16px + ${kb}px)`:``};", 'sheet reaches behind keyboard')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
