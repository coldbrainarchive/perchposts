#!/usr/bin/env python3
"""Patch v873 -> v879: fix the iPhone Safari search-bar bug (tapping search while scrolled down sometimes slid
the sticky header and search bar off the top of the screen).

What the v874-v878 readouts measured on the user's iPhone (Safari, iOS 27.2):
  - Every tap on search, Safari scrolls the page up 116pt as the keyboard opens. Harmless on its own.
  - Bad case: by 300ms Safari had put the page back to the tap position and shifted the visible area down
    116pt instead (visualViewport.offsetTop 116), carrying the header and search bar above the screen.
    No site code scrolls the page here; this is Safari undoing its own scroll.
  - The full readout (a fixed box whose transform and text were rewritten on every visualViewport
    resize/scroll and window scroll) prevented it every time. The same listeners without writing to the page
    did not, and the same box without updates did not. v875's extra space below the page didn't help either.

Fix: do what the readout did, invisibly. On iPhone/iPad only, a 1px fixed element is rewritten (transform +
text) on every visualViewport resize/scroll and window scroll, which keeps Safari's view of the page in step
while the keyboard animates.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v873.js'
dst = '_deploy/assets/index-DUcNPOLc-v879.js'
content = open(src, encoding='utf-8').read()

FIX = r'''
;(()=>{try{
if(!(window.CSS&&CSS.supports&&CSS.supports('-webkit-touch-callout','none')))return;
const vv=window.visualViewport;if(!vv)return;
const k=document.createElement('div');
k.setAttribute('aria-hidden','true');
k.style.cssText='position:fixed;left:0;top:0;width:1px;height:1px;overflow:hidden;font-size:1px;line-height:1px;color:transparent;pointer-events:none;z-index:2147483647;white-space:pre;';
document.body.appendChild(k);
const sync=()=>{const off=vv.offsetTop,vh=vv.height;k.style.transform='translateY('+Math.round(off+vh-2)+'px)';k.textContent=Math.round(scrollY)+' '+Math.round(off)+' '+Math.round(vh)+' '+innerHeight};
vv.addEventListener('resize',sync);vv.addEventListener('scroll',sync);
addEventListener('scroll',sync,{passive:true});
setInterval(sync,250);sync();
}catch(e){}})();
'''

open(dst, 'w', encoding='utf-8').write(content + FIX)
print('Wrote ' + dst)
