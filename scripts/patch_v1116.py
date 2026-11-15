#!/usr/bin/env python3
"""Patch v1115 -> v1116: the flap animation on post cards actually plays, like in the full-screen preview.
Tapping flap re-draws the card, which replaced the icon the animation had just started on; the animation now starts
just after that re-draw, on the icon that's on screen."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1115.js'
dst = '_deploy/assets/index-DUcNPOLc-v1116.js'
c = open(src, encoding='utf-8').read()
old = "if(/192,\\s*132,\\s*252/.test(b.getAttribute(`style`)||``))return;_ppFlapAnim(b)}catch(er){}},!0)"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "if(/192,\\s*132,\\s*252/.test(b.getAttribute(`style`)||``))return;requestAnimationFrame(()=>requestAnimationFrame(()=>_ppFlapAnim(b)))}catch(er){}},!0)"); print('OK: animate after the re-draw')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
