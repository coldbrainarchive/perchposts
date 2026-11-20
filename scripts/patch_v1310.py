#!/usr/bin/env python3
"""Patch v1309 -> v1310: no freeze mid-swipe with sound on in the post scroller.
Pausing the old video and starting the new one with sound happened at the start of the 0.34s slide animation; on
iPhone the audio switch stalls the screen, so the swipe froze halfway. With sound on, the switch now waits until the
slide has landed (370ms; rapid swipes cancel the pending switch). With sound off it stays instant."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1309.js'
dst = '_deploy/assets/index-DUcNPOLc-v1310.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
PAUSE = "try{track.querySelectorAll(`video`).forEach(v=>{if(!slides[i]||!slides[i].contains(v))v.pause()})}catch(e){}"
PLAY = "try{const cv=slides[i]&&slides[i].querySelector(`video`);if(cv&&cv.paused&&!cv._ppUserPaused){cv.muted=!_ppSnd();const pr=cv.play();pr&&pr.catch(()=>{if(!cv.muted){cv.muted=!0;cv.play().catch(()=>{})}})}}catch(e){}"
patch(PAUSE, "", 'move pause out')
patch(PLAY, "{const _vids=()=>{" + PAUSE + PLAY + "};clearTimeout(window._rvT);if(_ppSnd()&&track.style.transition&&track.style.transition!==`none`)window._rvT=setTimeout(_vids,370);else _vids()}", 'switch after the slide lands')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
