#!/usr/bin/env python3
"""Patch v1289 -> v1290: View post keeps at least 32px above the post scroller's bar.
A check on the post on screen: if View post is closer, that slide's bottom padding grows by the missing amount (long text shrinks and scrolls)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1289.js'
dst = '_deploy/assets/index-DUcNPOLc-v1290.js'
c = open(src, encoding='utf-8').read()
c += r"""
;(()=>{try{const NEED=32;
  // The slide centres its content between fixed top/bottom paddings; when View post sits closer than NEED to the bar,
  // grow this slide's bottom padding by the missing amount (repeats until it fits). Long text then shrinks and scrolls.
  const fix=s=>{const vp=s.querySelector(`.reel-vp`)||[...s.querySelectorAll(`a.reel-site`)].pop();const dock=document.querySelector(`.reel-dock`);if(!vp||!dock)return;
    const sr=s.getBoundingClientRect(),vr=vp.getBoundingClientRect(),dr=dock.getBoundingClientRect();if(!vr.height||!dr.height)return;
    const gap=dr.top-(vr.bottom-sr.top);if(gap>=NEED-1)return;
    const pb=parseFloat(getComputedStyle(s).paddingBottom)||0;s.style.setProperty(`padding-bottom`,(pb+Math.ceil(NEED-gap))+`px`,`important`);
    const d=s.querySelector(`.reel-desc`);d&&requestAnimationFrame(()=>{try{_reelFade(d)}catch(e){}})};
  setInterval(()=>{if(!document.documentElement.classList.contains(`reel-shown`))return;for(const s of document.querySelectorAll(`.reel-slide`)){const r=s.getBoundingClientRect();if(r.top>-5&&r.top<60)fix(s)}},250);
}catch(e){}})();
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
