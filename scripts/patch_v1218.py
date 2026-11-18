#!/usr/bin/env python3
"""Patch v1217 -> v1218: two-finger scroll is a flick: as soon as you start scrolling the scroller jumps to the next
(or previous) post, one post per scroll; the post no longer follows your fingers. Momentum is still ignored and a new
scroll during momentum still counts. Same sideways on a photo set."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1217.js'
dst = '_deploy/assets/index-DUcNPOLc-v1218.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("if(!edge&&Math.abs(wAcc)>Math.min(90,wCar.clientWidth*.16)){wCar._set(wCar._k+(wAcc>0?1:-1),!0);wAcc=0;wLock=!0;return}wCar._drag&&wCar._drag(-(edge?wAcc*.3:wAcc));return}",
      "if(Math.abs(wAcc)>12){if(!edge)wCar._set(wCar._k+(wAcc>0?1:-1),!0);wAcc=0;wLock=!0}return}", 'sideways flick')
patch("if(!edge&&Math.abs(wAcc)>Math.min(80,H()*.1)){const dir=wAcc>0?1:-1;wAcc=0;wLock=!0;go(i+dir);return}\n   track.style.transition=`none`;place(-(edge?wAcc*.3:wAcc),!1)},{passive:!1});",
      "if(Math.abs(wAcc)>12){const dir=wAcc>0?1:-1;wAcc=0;wLock=!0;if(!edge)go(i+dir);else{place(dir*-40,!0);setTimeout(()=>place(0,!0),160)}}},{passive:!1});", 'flick to the next post')
patch("const wEnd=()=>{wEndT=null;if(!wLock&&wAcc){if(wAx===`h`&&wCar&&wCar._set)wCar._set(wCar._k,!0);else place(0,!0)}wAcc=0;",
      "const wEnd=()=>{wEndT=null;wAcc=0;", 'nothing to spring back')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
