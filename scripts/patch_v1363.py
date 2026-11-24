#!/usr/bin/env python3
"""Patch v1362 -> v1363: tapping the chat filter pill again closes its menu; no ▾ on the filter pill."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1362.js'
dst = '_deploy/assets/index-DUcNPOLc-v1363.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("const off=e=>{if(!m.contains(e.target)){m.remove();document.removeEventListener(`pointerdown`,off,!0)}}",
      "const off=e=>{if(!m.isConnected){document.removeEventListener(`pointerdown`,off,!0);return}if(ref.current&&ref.current.contains(e.target))return;if(!m.contains(e.target)){m.remove();document.removeEventListener(`pointerdown`,off,!0)}}", 'pill toggles menu')
patch("body .lb-ic{", "body .ch-ctl .chf-b .cv{display:none!important}body .lb-ic{", 'no tiny arrow')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
