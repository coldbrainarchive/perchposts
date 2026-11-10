#!/usr/bin/env python3
"""Patch v980 -> v981: grabbing the scrubber while the chat is still coasting from a flick no longer fights
it. On grab the chat's own scrolling is switched off (which stops iOS momentum dead), the handle drives it
while you drag, and normal scrolling comes back when you let go."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v980.js'
dst = '_deploy/assets/index-DUcNPOLc-v981.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("hd.classList.add(`drag`);document.documentElement.classList.add(`sb-drag`);",
      "hd.classList.add(`drag`);document.documentElement.classList.add(`sb-drag`);{const _st=W.scrollTop;W.style.overflowY=`hidden`;void W.offsetHeight;W.scrollTop=_st;drag.w=W}",
      'stop momentum on grab')
patch("const end=e=>{if(!drag)return;drag=null;",
      "const end=e=>{if(!drag)return;if(drag.w)drag.w.style.overflowY=``;drag=null;", 'restore scrolling on release')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
