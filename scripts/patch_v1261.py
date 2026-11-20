#!/usr/bin/env python3
"""Patch v1260 -> v1261: smoother spin on phones.
- ~1.5x faster (10 s per half-turn instead of 15 s): very slow thin lines creep under a pixel per frame,
  which reads as stepping on mobile.
- The moving-lines overlay and the glowing logo under it each get their own GPU layer (will-change), so
  redrawing the lines doesn't make the phone repaint the blurred glow every frame."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1260.js'
dst = '_deploy/assets/index-DUcNPOLc-v1261.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const HALF=15000,RAMP=1800,", "const HALF=10000,RAMP=1500,", 'faster')
patch('style="position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible;pointer-events:none"',
      'style="position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible;pointer-events:none;will-change:transform;transform:translateZ(0)"', 'overlay layer')
patch("function setup(el,i){el.innerHTML=B.svg({...B.REST,noMer:1},`s`+i)+",
      "function setup(el,i){el.innerHTML=B.svg({...B.REST,noMer:1},`s`+i).replace(`<svg `,`<svg style=\"will-change:transform;transform:translateZ(0)\" `)+", 'base layer')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
