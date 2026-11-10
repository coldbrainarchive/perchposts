#!/usr/bin/env python3
"""Patch v972 -> v973:
- The chat's own scroll bar is hidden (the scrubber handle replaces it).
- Scrubbing never selects text: the date pill and handle can't be selected, and while you drag, text
  selection is off for the whole page (any selection is cleared when the drag starts)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v972.js'
dst = '_deploy/assets/index-DUcNPOLc-v973.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("try{hd.setPointerCapture(e.pointerId)}catch(x){}hd.classList.add(`drag`);",
      "try{hd.setPointerCapture(e.pointerId)}catch(x){}hd.classList.add(`drag`);document.documentElement.classList.add(`sb-drag`);try{getSelection().removeAllRanges()}catch(x){}", 'drag start: no selection')
patch("const end=e=>{if(!drag)return;drag=null;hd.classList.remove(`drag`);",
      "const end=e=>{if(!drag)return;drag=null;hd.classList.remove(`drag`);document.documentElement.classList.remove(`sb-drag`);", 'drag end')
c += r'''
;(()=>{try{document.addEventListener(`selectstart`,e=>{if(document.documentElement.classList.contains(`sb-drag`))e.preventDefault()});
const s=document.createElement(`style`);s.textContent=`
.chat-window{scrollbar-width:none;-ms-overflow-style:none}
.chat-window::-webkit-scrollbar{display:none;width:0;height:0}
.sb-date,.sb-handle{-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}
html.sb-drag,html.sb-drag *{-webkit-user-select:none!important;user-select:none!important;-webkit-touch-callout:none!important}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
