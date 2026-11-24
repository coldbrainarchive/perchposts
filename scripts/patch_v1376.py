#!/usr/bin/env python3
"""Patch v1375 -> v1376: no flash going back from the chirps to the post scroller (measured on the user's iPhone:
~100ms of the plain feed between the chat closing and the scroller reopening). When the chirps open, the scroller's
last screen is kept aside; on the way back it goes up at once as a still cover (no taps) over everything, the real
scroller reopens on the same post behind it, and the cover is removed two frames later."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1375.js'
dst = '_deploy/assets/index-DUcNPOLc-v1376.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
# keep the scroller's last screen when the chirps take over
patch("requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(()=>{ov.remove();body.overflow=prevOv},60)))",
      "requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(()=>{ov.remove();body.overflow=prevOv;window._reelShot={id,el:ov}},60)))", 'keep last screen')
# the still cover is not a live scroller
patch("if(document.querySelector(`.reel`))return;", "if(document.querySelector(`.reel:not(.reel-shot)`))return;", 'open ignores cover')
patch("if(!document.querySelector(`.reel`)){try{el.scrollIntoView({block:`center`})}catch(e){}_reelOpen(el)}}",
      "if(!document.querySelector(`.reel:not(.reel-shot)`)){try{el.scrollIntoView({block:`center`})}catch(e){}_reelOpen(el)}_ppShotOff()}", 'resume removes cover')
patch("else if(++n>50)clearInterval(t)},100)}catch(e){}})}catch(e){}})();",
      "else if(++n>50){clearInterval(t);_ppShotOff(!0)}},100)}catch(e){}})}catch(e){}})();", 'give-up removes cover')
# put the cover up the moment we go back to the scroller
patch("const rest={...st};delete rest.reelResume;try{history.replaceState(rest,``)}catch(e){}",
      "const rest={...st};delete rest.reelResume;try{history.replaceState(rest,``)}catch(e){}_ppShotOn(id);", 'cover on back')
c += r"""
function _ppShotOn(id){try{const s=window._reelShot;if(!s||s.id!==id||!s.el)return;const el=s.el;el.classList.add(`reel-shot`);el.style.pointerEvents=`none`;el.style.zIndex=`9600`;
 if(!el.isConnected)document.body.appendChild(el);document.documentElement.classList.add(`reel-shown`)}catch(e){}}
function _ppShotOff(fail){try{const s=window._reelShot;window._reelShot=null;if(!s||!s.el||!s.el.isConnected)return;
 requestAnimationFrame(()=>requestAnimationFrame(()=>{s.el.remove();if(fail&&!document.querySelector(`.reel:not(.reel-shot)`))document.documentElement.classList.remove(`reel-shown`)}))}catch(e){}}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
