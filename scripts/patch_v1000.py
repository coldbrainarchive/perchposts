#!/usr/bin/env python3
"""Patch v999 -> v1000: chat system lines ("👋 … left the huddle", "👥 … was added") are only as wide as their
text with round ends, so the flash when you open one from a notification is a pill around the words instead of a
full-width rectangle."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v999.js'
dst = '_deploy/assets/index-DUcNPOLc-v1000.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("if(e.username===`__system__`)return(0,L.jsx)(`div`,{style:{textAlign:`center`,color:`#64748b`,fontSize:12,padding:`6px 0`,fontStyle:`italic`,userSelect:`none`},children:e.content});",
      "if(e.username===`__system__`)return(0,L.jsx)(`div`,{className:`chat-sys`,style:{textAlign:`center`,color:`#64748b`,fontSize:12,padding:`5px 12px`,fontStyle:`italic`,userSelect:`none`},children:e.content});",
      'system line is a pill')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.chat-sys{align-self:center;width:fit-content;max-width:88%;margin:1px auto;border-radius:999px;box-sizing:border-box;line-height:1.35}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
