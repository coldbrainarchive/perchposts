#!/usr/bin/env python3
"""Patch v1140 -> v1141: notification badges: flaps show our purple flap icon instead of the 🪽 emoji
(worm notifications keep 🪱)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1140.js'
dst = '_deploy/assets/index-DUcNPOLc-v1141.js'
c = open(src, encoding='utf-8').read()
old = "padding:`0 2px`,boxSizing:`border-box`},children:e.icon}):null]});"
new = "padding:`0 2px`,boxSizing:`border-box`},children:e.icon===`🪽`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}):e.icon}):null]});"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, new); print('OK: flap badge')
c = c.replace("body .lb-ic{", "body .n-flap{display:inline-flex;color:#c084fc}body .n-flap .ri{width:12px;height:12px;display:block}body .lb-ic{", 1); print('OK: styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
