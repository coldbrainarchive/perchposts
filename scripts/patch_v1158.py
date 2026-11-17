#!/usr/bin/env python3
"""Patch v1157 -> v1158: the Worm wallet's top handle works: tapping it closes the wallet, and dragging it down
(more than ~70px, or a quick flick) closes it too; a short drag springs back."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1157.js'
dst = '_deploy/assets/index-DUcNPOLc-v1158.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch(" const ww=_wwPanel({kind:`p`,id,own,done:close});sh.append(ww.el);",
      " const ww=_wwPanel({kind:`p`,id,own,done:close});const grab=document.createElement(`button`);grab.type=`button`;grab.className=`ww-grab`;grab.setAttribute(`aria-label`,`Close the worm wallet`);sh.append(grab,ww.el);\n"
      " {let y0=null,t0=0,dy=0,moved=!1;const end=()=>{if(y0==null)return;const fast=dy>30&&Date.now()-t0<250;sh.style.transition=``;if(dy>70||fast){close();sh.style.transform=`translateY(100%)`}else sh.style.transform=``;y0=null};\n"
      "  grab.addEventListener(`touchstart`,e=>{y0=e.touches[0].clientY;t0=Date.now();dy=0;moved=!1;sh.style.transition=`none`},{passive:!0});\n"
      "  grab.addEventListener(`touchmove`,e=>{if(y0==null)return;dy=Math.max(0,e.touches[0].clientY-y0);if(dy>4)moved=!0;sh.style.transform=`translateY(${dy}px)`;e.preventDefault()},{passive:!1});\n"
      "  grab.addEventListener(`touchend`,()=>{if(moved)end();else{sh.style.transition=``;y0=null}});grab.addEventListener(`touchcancel`,end);grab.onclick=e=>{e.stopPropagation();if(!moved)close()}}", 'working handle')
patch("body .ww-ov .ww-sheet::before{content:'';display:block;width:38px;height:5px;border-radius:999px;background:#3a3d48;margin:-6px auto 12px}",
      "body .ww-grab{display:block;width:calc(100% + 36px);height:30px;margin:-18px -18px 2px;padding:0;border:0;background:none;cursor:pointer;touch-action:none;position:relative}"
      "body .ww-grab::after{content:'';position:absolute;left:50%;top:12px;width:40px;height:5px;margin-left:-20px;border-radius:999px;background:#4b4f5c;transition:background .15s}"
      "body .ww-grab:hover::after,body .ww-grab:active::after{background:#6b7080}body .ww-ov .ww-sheet{transition:transform .22s cubic-bezier(.2,.8,.3,1)}", 'handle styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
