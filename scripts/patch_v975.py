#!/usr/bin/env python3
"""Patch v974 -> v975: less on screen while scrolling.
- The date pill no longer pops up while you scroll; it only shows (above the handle) while you drag it.
- The scrubber handle is half as thin at rest (8px) so it covers less of the chirps; its touch area stays
  as wide as before, and it still swells to the same big size when you grab it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v974.js'
dst = '_deploy/assets/index-DUcNPOLc-v975.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('pill.classList.toggle(`on`,!!pill.textContent);', 'pill.classList.toggle(`on`,!!drag&&!!pill.textContent);', 'date only while dragging')
patch('hd.style.left=(r.right-22)+`px`;', 'hd.style.left=(r.right-14)+`px`;', 'thin handle position')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.sb-handle{width:8px}
.sb-handle::after{inset:-14px -16px -14px -18px}
.sb-handle.drag{transform:scale(3.3,1.25)}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
