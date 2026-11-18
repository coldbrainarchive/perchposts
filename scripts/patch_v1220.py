#!/usr/bin/env python3
"""Patch v1219 -> v1220: close the scroller by swiping RIGHT (it slides off to the right), not left.
On a photo set, swiping right on the first photo closes it too (on other photos it goes back a photo)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1219.js'
dst = '_deploy/assets/index-DUcNPOLc-v1220.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("if(axis===`text`)return;if(axis===`h`&&car&&car._drag){cdx=x-sx;car._drag(cdx);e.preventDefault();return}"
      "if(axis===`h`&&!car){cdx=x-sx;const d=Math.min(0,cdx);",
      "if(axis===`text`)return;const cls=axis===`h`&&(!car||(car._k===0&&x-sx>0&&!car._mv));if(axis===`h`&&car&&car._drag&&!cls){car._mv=!0;cdx=x-sx;car._drag(cdx);e.preventDefault();return}"
      "if(cls){cdx=x-sx;const d=Math.max(0,cdx);", 'swipe right follows the finger')
patch("if(axis===`h`&&!car){const fast=cdx<-30&&-cdx/Math.max(1,Date.now()-st)>.45,go2=cdx<-innerWidth*.25||fast;",
      "if(car)car._mv=!1;if(axis===`h`&&ov.style.transform){const fast=cdx>30&&cdx/Math.max(1,Date.now()-st)>.45,go2=cdx>innerWidth*.25||fast;", 'decide on the right swipe')
patch("if(go2){ov.style.transform=`translate3d(${-innerWidth}px,0,0)`;", "if(go2){ov.style.transform=`translate3d(${innerWidth}px,0,0)`;", 'slide off to the right')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
