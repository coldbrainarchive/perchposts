#!/usr/bin/env python3
"""Patch v1290 -> v1291: the View post gap fix no longer pops in.
It runs before paint: when slides are added (MutationObserver), when a slide's photo loads (load event, capture),
and repeats until settled, on every slide (also the ones just off screen), not only the visible one every 250ms."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1290.js'
dst = '_deploy/assets/index-DUcNPOLc-v1291.js'
c = open(src, encoding='utf-8').read()
i = c.rindex(';(()=>{try{const NEED=32;')
j = c.index('}catch(e){}})();', i) + len('}catch(e){}})();')
c = c[:i] + r""";(()=>{try{const NEED=32;
  const fix=s=>{const vp=s.querySelector(`.reel-vp`)||[...s.querySelectorAll(`a.reel-site`)].pop();const dock=document.querySelector(`.reel-dock`);if(!vp||!dock)return!1;
    const sr=s.getBoundingClientRect(),vr=vp.getBoundingClientRect(),dr=dock.getBoundingClientRect();if(!vr.height||!dr.height||!sr.height)return!1;
    const gap=dr.top-(vr.bottom-sr.top);if(gap>=NEED-1)return!1;
    const pb=parseFloat(getComputedStyle(s).paddingBottom)||0;s.style.setProperty(`padding-bottom`,(pb+Math.ceil(NEED-gap))+`px`,`important`);return!0};
  const settle=s=>{let n=0;while(n<6&&fix(s))n++;if(n){const d=s.querySelector(`.reel-desc`);d&&requestAnimationFrame(()=>{try{_reelFade(d)}catch(e){}})}};
  const all=()=>{for(const s of document.querySelectorAll(`.reel .reel-slide`))settle(s)};
  new MutationObserver(ms=>{if(!document.querySelector(`.reel`))return;for(const m of ms)for(const n of m.addedNodes){if(n.nodeType===1&&(n.classList.contains(`reel`)||n.classList.contains(`reel-slide`)||n.querySelector&&n.querySelector(`.reel-slide`))){all();return}}}).observe(document.body,{childList:!0,subtree:!0});
  document.addEventListener(`load`,e=>{const t=e.target;if(t&&(t.tagName===`IMG`||t.tagName===`VIDEO`)){const s=t.closest&&t.closest(`.reel-slide`);s&&settle(s)}},!0);
  document.addEventListener(`loadedmetadata`,e=>{const s=e.target&&e.target.closest&&e.target.closest(`.reel-slide`);s&&settle(s)},!0);
  addEventListener(`resize`,()=>{if(document.querySelector(`.reel`))requestAnimationFrame(all)});
  setInterval(()=>{if(document.documentElement.classList.contains(`reel-shown`))all()},500);
}catch(e){}})();""" + c[j:]
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
