#!/usr/bin/env python3
"""Patch v1285 -> v1286: the pills at the top of the post scroller are tappable.
- Bird name pill: opens the bird's card above the scroller ([data-gpb]).
- Tag / country pills: close the scroller and filter the feed, by clicking the matching pill on the feed card
  (same as tapping it there). Works in the info panel's cloned header too (click delegation on the overlay)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1285.js'
dst = '_deploy/assets/index-DUcNPOLc-v1286.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("if(out.some(o=>o.t===t))continue;out.push({t,c:bg})}return out}catch(e){return[]}}",
      "if(out.some(o=>o.t===t))continue;out.push({t,c:bg,el:x})}return out}catch(e){return[]}}", 'keep source pill')
patch("const sp=document.createElement(`span`);sp.className=`reel-tag`;sp.textContent=g.t;sp.style.color=g.c;sp.style.borderColor=g.c;tr.appendChild(sp)",
      "const sp=document.createElement(`span`);sp.className=`reel-tag`;sp.textContent=g.t;sp.style.color=g.c;sp.style.borderColor=g.c;if(g.el){const L2=window._reelTagEls||(window._reelTagEls=[]);sp.dataset.ti=L2.push(g.el)-1;sp.setAttribute(`role`,`button`)}tr.appendChild(sp)", 'tag pill index')
patch("const w=document.createElement(`span`);w.className=`reel-tag reel-whotag`;w.style.color=d.who.c;w.style.borderColor=d.who.c;",
      "const w=document.createElement(`span`);w.className=`reel-tag reel-whotag`;w.style.color=d.who.c;w.style.borderColor=d.who.c;if(d.who.n&&!/^Anon #/.test(d.who.n)&&d.who.n!==`Extinct Bird`){w.dataset.gpb=d.who.n;w.setAttribute(`role`,`button`)}", 'who pill opens card')
patch("const goPost=id=>{pendingPost=id;close()};",
      "const goPost=id=>{pendingPost=id;close()};ov.addEventListener(`click`,e=>{const t=e.target.closest&&e.target.closest(`.reel-tag[data-ti]`);if(!t)return;const el=(window._reelTagEls||[])[+t.dataset.ti];if(!el||!el.isConnected)return;e.preventDefault();e.stopPropagation();window._rpt=el;close()},!0);", 'tag tap closes + filters')
patch("if(pendingNoAuth)setTimeout(()=>window.dispatchEvent(new CustomEvent(`like-no-auth`)),60);",
      "if(window._rpt){const el=window._rpt;window._rpt=null;setTimeout(()=>{try{el.isConnected&&el.click()}catch(e){}},40)}if(pendingNoAuth)setTimeout(()=>window.dispatchEvent(new CustomEvent(`like-no-auth`)),60);", 'apply filter after close')
patch("body .lb-ic{", "body .reel-tag[data-ti],body .reel-tag[data-gpb]{cursor:pointer}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
