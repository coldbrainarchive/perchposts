#!/usr/bin/env python3
"""Patch v977 -> v978: Oldest / Newest work while the chat is still coasting from a flick. iOS Safari ignores
programmatic scrolls during momentum scrolling, so the jump first stops the momentum (scrolling switched off
for a frame), then jumps straight to the end (and again next frame in case Safari applied a last bit of
momentum)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v977.js'
dst = '_deploy/assets/index-DUcNPOLc-v978.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('if(e&&e.lastElementChild){e.lastElementChild.scrollIntoView();x(!1);}', 'if(e&&e.lastElementChild){_sbJump(e,1);x(!1);}', 'Oldest')
patch('if(e&&e.firstElementChild){e.firstElementChild.scrollIntoView();x(!0);}', 'if(e&&e.firstElementChild){_sbJump(e,0);x(!0);}', 'Newest')
c += r'''
function _sbJump(w,old){const go=()=>{w.scrollTop=old?-(w.scrollHeight):0};
 w.style.overflowY=`hidden`;void w.offsetHeight;go();
 requestAnimationFrame(()=>{w.style.overflowY=``;go();requestAnimationFrame(go)})}
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
