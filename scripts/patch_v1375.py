#!/usr/bin/env python3
"""Patch v1374 -> v1375: the flash opening chirps from the scroller after swiping down, fixed for real (measured on
the user's iPhone frame by frame). When the hidden feed is scrolled down and the page jumps to the top in the same
moment the chat pins the page, Safari snaps back to the old scroll for one frame, pulling the scroller off screen.
Now the feed is scrolled to the top first and Safari gets ~3 frames + 120ms to settle (only when it was scrolled),
then the chat opens. Tested on the phone with a 400ms gap: no bad frames."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1374.js'
dst = '_deploy/assets/index-DUcNPOLc-v1375.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("try{window.scrollTo(0,0)}catch(e){}tcm&&prevTc&&tcm.setAttribute(`content`,prevTc);document.documentElement.classList.remove(`reel-shown`);const a=_reelChatA(id);",
      "const _sc=window.scrollY>0;try{window.scrollTo(0,0)}catch(e){}const go2=()=>{tcm&&prevTc&&tcm.setAttribute(`content`,prevTc);document.documentElement.classList.remove(`reel-shown`);const a=_reelChatA(id);", 'split')
patch("ov.remove();body.overflow=prevOv},60)))}},40)};",
      "ov.remove();body.overflow=prevOv},60)))}},40)};if(_sc)requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(go2,120))));else go2()};", 'wait if scrolled')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
