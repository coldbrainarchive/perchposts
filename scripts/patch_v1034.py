#!/usr/bin/env python3
"""Patch v1033 -> v1034: easier text scrolling in the full-screen link view, plus a scroll bar.
- Fix: the first few pixels of every swipe were blocked before deciding "scroll the text or change post"; on
  iPhone that cancels the text's own scrolling for the whole swipe, so it often felt stuck. Now a swipe that starts
  on scrollable text is left to the phone until it's clear it's a post swipe.
- A thin purple scroll bar beside long text shows how far through you are (only when there's more to read)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1033.js'
dst = '_deploy/assets/index-DUcNPOLc-v1034.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('place(edge?dy*.3:dy,!1)}e.preventDefault()},{passive:!1});',
      'place(edge?dy*.3:dy,!1)}if(axis===`v`||axis===`h`||!txt)e.preventDefault()},{passive:!1});',
      "don't block the text's own scrolling")
patch("if(d.desc){const t=document.createElement(`div`);t.className=`reel-desc`;t.textContent=d.desc;t.addEventListener(`scroll`,()=>_reelFade(t),{passive:!0});inner.appendChild(t)}",
      "if(d.desc){const w=document.createElement(`div`);w.className=`reel-descw`;const t=document.createElement(`div`);t.className=`reel-desc`;t.textContent=d.desc;"
      "const bar=document.createElement(`div`);bar.className=`reel-bar`;bar.hidden=!0;const th=document.createElement(`div`);th.className=`reel-thumb`;bar.appendChild(th);"
      "t.addEventListener(`scroll`,()=>_reelFade(t),{passive:!0});w.append(t,bar);inner.appendChild(w)}",
      'text with a scroll bar')
patch("function _reelFade(d){d.classList.toggle(`more`,d.scrollTop+d.clientHeight<d.scrollHeight-2)}",
      "function _reelFade(d){d.classList.toggle(`more`,d.scrollTop+d.clientHeight<d.scrollHeight-2);const bar=d.nextElementSibling;if(!bar||!bar.classList.contains(`reel-bar`))return;"
      "const sh=d.scrollHeight,ch=d.clientHeight;if(sh<=ch+2){bar.hidden=!0;return}bar.hidden=!1;const bh=bar.clientHeight||ch,tH=Math.max(28,bh*ch/sh),tT=(d.scrollTop/(sh-ch))*(bh-tH);"
      "const th=bar.firstChild;th.style.height=tH+`px`;th.style.transform=`translateY(${Math.max(0,Math.min(bh-tH,tT))}px)`}",
      'scroll bar follows the text')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel-descw{position:relative;display:flex;flex-direction:column;min-height:0;flex:0 1 auto;margin-top:10px}
.reel-descw .reel-desc{margin-top:0;padding-right:14px}
.reel-bar{position:absolute;top:2px;bottom:2px;right:0;width:4px;border-radius:3px;background:rgba(255,255,255,.08);pointer-events:none}
.reel-bar[hidden]{display:none}
.reel-thumb{position:absolute;left:0;right:0;top:0;border-radius:3px;background:#c084fc;opacity:.9}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
