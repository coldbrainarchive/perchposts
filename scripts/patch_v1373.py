#!/usr/bin/env python3
"""Patch v1371 -> v1373 (v1372's prefetch dropped — no visible change for the user): the brief dark flash when
tapping chirps in the post scroller. The scroller was removed as soon as the chat screen existed, before its chirps
had drawn, so an empty chat showed for a frame or two. It now stays on top until the chat has drawn its chirps (or
"No chirps yet") plus two frames, then goes away in one step."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1371.js'
dst = '_deploy/assets/index-DUcNPOLc-v1373.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("if(document.querySelector(`.comments-shell.chat-full`)||++n>60){clearInterval(t);ov.classList.remove(`in`);setTimeout(()=>{ov.remove();body.overflow=prevOv},180)}},50)",
      "const sh=document.querySelector(`.comments-shell.chat-full`),w=sh&&sh.querySelector(`.chat-window`);"
      "if(w&&(w.querySelector(`.chat-msg`)||/No chirps yet/.test(w.textContent))||++n>80){clearInterval(t);"
      "requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(()=>{ov.remove();body.overflow=prevOv},60)))}},40)",
      'wait for chirps to draw')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
