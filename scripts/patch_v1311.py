#!/usr/bin/env python3
"""Patch v1310 -> v1311: with sound on, the incoming video no longer shows as paused while the slide moves.
It starts playing muted right away (cheap, like sound-off); when the slide lands (370ms) the old video pauses and the
new one's sound turns on (if the phone refuses, it keeps playing muted). The play button is hidden in between."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1310.js'
dst = '_deploy/assets/index-DUcNPOLc-v1311.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
old = "clearTimeout(window._rvT);if(_ppSnd()&&track.style.transition&&track.style.transition!==`none`)window._rvT=setTimeout(_vids,370);else _vids()}"
new = ("clearTimeout(window._rvT);if(_ppSnd()&&track.style.transition&&track.style.transition!==`none`){"
       "const s0=slides[i],nv=s0&&s0.querySelector(`video`);"
       "if(nv&&nv.paused&&!nv._ppUserPaused){s0.classList.add(`reel-arriving`);nv.muted=!0;nv.play().catch(()=>{})}"
       "window._rvT=setTimeout(()=>{try{track.querySelectorAll(`video`).forEach(v=>{if(!slides[i]||!slides[i].contains(v))v.pause()})}catch(e){}"
       "const s1=slides[i],cv=s1&&s1.querySelector(`video`);s0&&s0.classList.remove(`reel-arriving`);"
       "if(cv&&!cv._ppUserPaused&&_ppSnd()){cv.muted=!1;if(cv.paused){const pr=cv.play();pr&&pr.catch(()=>{cv.muted=!0;cv.play().catch(()=>{})})}}"
       "else if(cv&&cv.paused&&!cv._ppUserPaused)_vids()},370)}else _vids()}")
patch(old, new, 'start muted now, sound on landing')
patch("body .lb-ic{", "body .reel-slide.reel-arriving .reel-playic{opacity:0!important}body .lb-ic{", 'hide play icon while arriving')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
