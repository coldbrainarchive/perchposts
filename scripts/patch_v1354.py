#!/usr/bin/env python3
"""Patch v1353 -> v1354: the story dots on the globe logo fade out while the bird animation plays (the logo's
_ppBusy flag) and come back when it's done."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1353.js'
dst = '_deploy/assets/index-DUcNPOLc-v1354.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch(" const st=document.createElement(`style`);document.head.appendChild(st);\n let last=null;",
      " const st=document.createElement(`style`);document.head.appendChild(st);\n // while the bird animation plays, the dots fade out\n const bs=document.createElement(`style`);bs.textContent=`html.gl-bird .pp-logo::after{animation:glOut .25s ease-out forwards!important}\n@keyframes glOut{to{opacity:0}}`;document.head.appendChild(bs);\n let last=null;", 'bird css')
patch(" let spinning=!1;const tick=()=>{const on=!!(window._ppSpin&&window._ppSpin.on);if(on||spinning)draw();spinning=on;requestAnimationFrame(tick)};",
      " let spinning=!1,bird=!1;const tick=()=>{const on=!!(window._ppSpin&&window._ppSpin.on);if(on||spinning)draw();spinning=on;\n  const b=!!(document.querySelector(`.pp-logo`)||{})._ppBusy;if(b!==bird){bird=b;document.documentElement.classList.toggle(`gl-bird`,b)}requestAnimationFrame(tick)};", 'bird watch')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
