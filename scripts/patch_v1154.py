#!/usr/bin/env python3
"""Patch v1153 -> v1154: Worm wallet fixes.
- The lifted post is scaled down to fit the space above the sheet (it was clipped: bottom on phones, side on
  desktop, where the chirp sheet's 520px limit squeezed it).
- Quick picks are 1 / 5 / 10 / 20 (no "All").
- Small polish: "worms" under the number box, clearer disabled −/+, the sheet's top grab handle."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1153.js'
dst = '_deploy/assets/index-DUcNPOLc-v1154.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# fit the lifted post
patch(" ov.append(top,sh);document.body.append(ov);requestAnimationFrame(()=>ov.classList.add(`in`));\n ov.addEventListener(`click`,e=>{if(e.target===ov||e.target.closest(`.ww-top`))close()})}",
      " ov.append(top,sh);document.body.append(ov);requestAnimationFrame(()=>ov.classList.add(`in`));\n"
      " const fit=()=>{const wr=top.querySelector(`.ww-post`);if(!wr||shut)return;wr.style.transform=``;const cs=getComputedStyle(top),W=top.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight),H=top.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom),s=Math.min(1,W/wr.offsetWidth,H/wr.offsetHeight);wr.style.transform=s<1?`scale(${s})`:``};\n"
      " fit();[60,300,900].forEach(t=>setTimeout(fit,t));top.querySelectorAll(`img`).forEach(im=>im.complete||im.addEventListener(`load`,fit));addEventListener(`resize`,fit);\n"
      " ov.addEventListener(`click`,e=>{if(e.target===ov||e.target.closest(`.ww-top`))close()})}", 'scale the post to fit')
# 20 instead of All
patch("<button type=\"button\" data-q=\"10\">10</button><button type=\"button\" data-q=\"all\">All</button></div>",
      "<button type=\"button\" data-q=\"10\">10</button><button type=\"button\" data-q=\"20\">20</button></div>", '20 instead of All')
# "worms" caption under the number
patch("<input class=\"ww-in\" type=\"text\" inputmode=\"numeric\" pattern=\"[0-9]*\" autocomplete=\"off\" aria-label=\"How many worms\" value=\"1\">",
      "<label class=\"ww-inw\"><input class=\"ww-in\" type=\"text\" inputmode=\"numeric\" pattern=\"[0-9]*\" autocomplete=\"off\" aria-label=\"How many worms\" value=\"1\"><span class=\"ww-unit\">worms</span></label>", 'caption')
patch("inp.addEventListener(`input`,()=>{", "const un=el.querySelector(`.ww-unit`);inp.addEventListener(`input`,()=>{", 'caption hook')
patch("const[mn,pl]=el.querySelectorAll(`.ww-st`);mn.disabled=cnt<=1;", "const un2=el.querySelector(`.ww-unit`);if(un2)un2.textContent=cnt===1?`worm`:`worms`;const[mn,pl]=el.querySelectorAll(`.ww-st`);mn.disabled=cnt<=1;", 'worm / worms')
css = ("body .ww-ov .ww-top{max-width:none;align-items:center;justify-content:flex-end}"
       "body .ww-ov .ww-post{max-height:none;overflow:visible;flex-shrink:0;transform-origin:center bottom}"
       "body .ww-inw{flex:1;min-width:0;position:relative;display:block}body .ww-inw .ww-in{width:100%;height:58px;padding:0 0 16px;line-height:1}body .ww-ov .ww-st,body .ww .ww-st{height:58px;width:52px}"
       "body .ww-unit{position:absolute;left:0;right:0;bottom:7px;text-align:center;font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#64748b;pointer-events:none}"
       "body .ww-st:disabled{opacity:1;color:#4b5060;background:#1c1d23;border-color:#2c2e37}"
       "body .ww-ov .ww-sheet::before{content:'';display:block;width:38px;height:5px;border-radius:999px;background:#3a3d48;margin:-6px auto 12px}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
