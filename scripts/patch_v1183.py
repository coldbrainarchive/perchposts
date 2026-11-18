#!/usr/bin/env python3
"""Patch v1182 -> v1183: the Bird ID card can be swiped down to close (it follows your finger; let go past
~90px, or flick down, and it slides away; otherwise it springs back)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1182.js'
dst = '_deploy/assets/index-DUcNPOLc-v1183.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
SWIPE = r''';(()=>{try{if(window._bcSwipe)return;window._bcSwipe=1;let st=null;
 const card=t=>{const sh=t&&t.closest&&t.closest(`.bc-sheet`);return sh&&sh.firstElementChild&&sh.firstElementChild.contains(t)?[sh,sh.firstElementChild]:null};
 document.addEventListener(`touchstart`,e=>{const h=card(e.target);if(!h||e.touches.length!==1)return;let n=e.target;while(n&&n!==h[1]){if(n.scrollTop>0)return;n=n.parentElement}
  st={sh:h[0],el:h[1],y:e.touches[0].clientY,x:e.touches[0].clientX,t:performance.now(),dy:0,on:!1}},{passive:!0});
 document.addEventListener(`touchmove`,e=>{if(!st)return;const dy=e.touches[0].clientY-st.y,dx=e.touches[0].clientX-st.x;
  if(!st.on){if(Math.abs(dx)>Math.abs(dy)||dy<6){if(dy<-6||Math.abs(dx)>10)st=null;return}st.on=!0;st.el.style.transition=`none`}
  st.dy=Math.max(0,dy);st.el.style.transform=`translateY(${st.dy}px)`;e.preventDefault()},{passive:!1});
 const end=()=>{if(!st)return;const s=st;st=null;if(!s.on)return;const v=s.dy/Math.max(1,performance.now()-s.t);
  s.el.style.transition=`transform .22s cubic-bezier(.3,.7,.2,1)`;
  if(s.dy>90||(s.dy>30&&v>.6)){s.el.style.transform=`translateY(110%)`;s.sh.style.transition=`opacity .22s`;s.sh.style.opacity=`0`;setTimeout(()=>{s.sh.click()},200)}
  else{s.el.style.transform=``;setTimeout(()=>{s.el.style.transition=``},240)}};
 document.addEventListener(`touchend`,end);document.addEventListener(`touchcancel`,end)}catch(e){}})();
'''
patch("function _hxSheet(post,members){", SWIPE + "function _hxSheet(post,members){", 'swipe down to close')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
