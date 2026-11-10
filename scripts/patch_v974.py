#!/usr/bin/env python3
"""Patch v973 -> v974: scrubbing with a thumb.
- While you drag, the date pill sits above the handle (right-aligned to it) instead of beside it, so your
  thumb doesn't cover it; it's a bit bigger too.
- Touching the handle makes it swell with a springy squish (anchored to the right edge) and it springs
  back when you let go."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v973.js'
dst = '_deploy/assets/index-DUcNPOLc-v974.js'
c = open(src, encoding='utf-8').read()
old = "if(drag){pill.style.left=(r.right-34)+`px`;pill.style.top=(y+hh/2)+`px`;pill.classList.add(`by`)}"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "if(drag){pill.style.left=(r.right-4)+`px`;pill.style.top=Math.max(r.top+8,y-14)+`px`;pill.classList.add(`by`)}")
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.sb-date.by{transform:translate(-100%,-100%);height:32px;line-height:32px;font-size:14px;padding:0 15px;border-color:#c084fc;box-shadow:0 6px 18px rgba(0,0,0,.45)}
.sb-handle{transform-origin:right center;transition:opacity .2s,background .15s,transform .32s cubic-bezier(.3,1.7,.45,1)}
.sb-handle.drag{transform:scale(1.65,1.25);transition:opacity .2s,background .15s,transform .26s cubic-bezier(.3,1.9,.45,1)}
@media (prefers-reduced-motion: reduce){.sb-handle,.sb-handle.drag{transition:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
