#!/usr/bin/env python3
"""Patch v1221 -> v1223: the scroller's close button is a back arrow ‹ (chevron) instead of ✕; same place, same job."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1221.js'
dst = '_deploy/assets/index-DUcNPOLc-v1223.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("xb.setAttribute(`aria-label`,`Close`);xb.innerHTML=`<svg viewBox=\"0 0 24 24\" width=\"18\" height=\"18\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.4\" stroke-linecap=\"round\"><path d=\"M6 6l12 12M18 6 6 18\"/></svg>`;",
      "xb.setAttribute(`aria-label`,`Back`);xb.innerHTML=`<svg viewBox=\"0 0 24 24\" width=\"22\" height=\"22\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.4\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14.5 5.5 8 12l6.5 6.5\"/></svg>`;", 'back chevron')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
