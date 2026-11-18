#!/usr/bin/env python3
"""Patch v1197 -> v1198: the scroller remembers your sound setting. Turn sound on (or off) on one video and every
video after that starts the same way, including next time you open the scroller (saved on this device).
If a phone refuses to start a video with sound, it falls back to muted."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1197.js'
dst = '_deploy/assets/index-DUcNPOLc-v1198.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("function _reelCollect(){", "function _ppSnd(){try{return localStorage.getItem(`pp_reel_sound`)===`1`}catch(e){return!1}}\nfunction _reelCollect(){", 'saved setting')
patch("v.muted=!0;v.defaultMuted=!0;v.setAttribute(`muted`,``);", "v.muted=!_ppSnd();v.defaultMuted=v.muted;if(v.muted)v.setAttribute(`muted`,``);", 'new videos use it')
patch("if(cv&&cv.paused&&!cv._ppUserPaused){const pr=cv.play();pr&&pr.catch(()=>{})}",
      "if(cv&&cv.paused&&!cv._ppUserPaused){cv.muted=!_ppSnd();const pr=cv.play();pr&&pr.catch(()=>{if(!cv.muted){cv.muted=!0;cv.play().catch(()=>{})}})}", 'autoplay uses it')
patch("mu.addEventListener(`click`,e=>{e.stopPropagation();vv.muted=!vv.muted;",
      "mu.addEventListener(`click`,e=>{e.stopPropagation();vv.muted=!vv.muted;try{localStorage.setItem(`pp_reel_sound`,vv.muted?`0`:`1`)}catch(_){}", 'sound button saves it')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
