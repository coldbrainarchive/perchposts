#!/usr/bin/env python3
"""Patch v1207 -> v1208 (scroller):
- Top fade: no faint fade behind the ✕ any more; the top stays black past the ✕ and then fades in quickly
  (the harder fade lower down is kept).
- Info panel: tighter spacing (smaller padding and gaps; VIEW POST line no longer 35px tall). Font sizes unchanged.
- Tapping anywhere in the panel's info area opens the post (like VIEW POST).
- A grab handle on top of the panel: drag it down (or tap) to fold the info away to just the bar, drag up / tap to
  bring it back. Remembered on this device."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1207.js'
dst = '_deploy/assets/index-DUcNPOLc-v1208.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("rpan.append(rpw,dock);ov.appendChild(rpan);",
      "const rgrab=document.createElement(`div`);rgrab.className=`reel-grab`;rgrab.setAttribute(`role`,`button`);rgrab.setAttribute(`aria-label`,`Show or hide the post details`);rpan.append(rgrab,rpw,dock);ov.appendChild(rpan);"
      "const rpCol=v=>{rpan.classList.toggle(`collapsed`,v);try{localStorage.setItem(`pp_reel_info`,v?`0`:`1`)}catch(e){}};try{rpan.classList.toggle(`collapsed`,localStorage.getItem(`pp_reel_info`)===`0`)}catch(e){}"
      "{let gy=null,gd=0;rgrab.addEventListener(`touchstart`,e=>{e.stopPropagation();gy=e.touches[0].clientY;gd=0},{passive:!0});"
      "rgrab.addEventListener(`touchmove`,e=>{e.stopPropagation();e.preventDefault();if(gy!=null)gd=e.touches[0].clientY-gy},{passive:!1});"
      "rgrab.addEventListener(`touchend`,e=>{e.stopPropagation();if(gy==null)return;const d=gd;gy=null;if(d>24)rpCol(!0);else if(d<-24)rpCol(!1)});"
      "rgrab.addEventListener(`click`,e=>{e.stopPropagation();rpCol(!rpan.classList.contains(`collapsed`))})}", 'grab handle')
patch("rpi.addEventListener(`click`,e=>{const a=e.target.closest&&e.target.closest(`.reel-site`);if(!a)return;e.preventDefault();",
      "rpi.addEventListener(`click`,e=>{e.preventDefault();", 'whole info area opens the post')
css = ("body .reel-view{-webkit-mask-image:linear-gradient(to bottom,transparent 0,transparent calc(44px + env(safe-area-inset-top)),#000 calc(96px + env(safe-area-inset-top)),#000 calc(100% - 66px - env(safe-area-inset-bottom)),rgba(0,0,0,.35) calc(100% - 22px - env(safe-area-inset-bottom)),transparent 100%)!important;"
       "mask-image:linear-gradient(to bottom,transparent 0,transparent calc(44px + env(safe-area-inset-top)),#000 calc(96px + env(safe-area-inset-top)),#000 calc(100% - 66px - env(safe-area-inset-bottom)),rgba(0,0,0,.35) calc(100% - 22px - env(safe-area-inset-bottom)),transparent 100%)!important}"
       "body .reel-pinfo-in{padding:2px 12px 10px!important;cursor:pointer}"
       "body .reel-pinfo-in .reel-head{margin:0 0 8px!important}"
       "body .reel-pinfo-in a.reel-site{margin-top:6px!important;padding:0!important;line-height:1!important}"
       "body .reel-pinfo-in a.reel-site .reel-site-ar{margin:-3px 0}"
       "body .reel-grab{display:none;height:16px;align-items:center;justify-content:center;cursor:grab;touch-action:none;-webkit-tap-highlight-color:transparent}"
       "body .reel-panel.open .reel-grab{display:flex}"
       "body .reel-grab::before{content:'';width:36px;height:4px;border-radius:9px;background:rgba(148,163,184,.65)}"
       "body .reel-panel.collapsed .reel-pinfo-w{grid-template-rows:0fr!important}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
