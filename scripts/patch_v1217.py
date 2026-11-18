#!/usr/bin/env python3
"""Patch v1216 -> v1217 (scroller on computers):
- Wide screens: the scroller is a centred phone-shaped column (9:16, as tall as the window) with black on both sides,
  so photos / videos aren't blown up and cropped across the whole window.
- Trackpad / wheel: the post follows your scroll, moves on once you pass a short distance (one post per gesture) and
  springs back if you stop short. Momentum after a swipe is ignored, but a fresh swipe during that momentum is
  recognised straight away. Same for sideways scrolling through a photo set."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1216.js'
dst = '_deploy/assets/index-DUcNPOLc-v1217.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
i = c.index("{let wAcc=0,wT=0,wLock=0;ov.addEventListener(`wheel`,"); j = c.index("let md=null;", i)
NEW = r'''{let wAcc=0,wLock=!1,wPrev=0,wEndT=null,wAx=null,wCar=null;
  const wEnd=()=>{wEndT=null;if(!wLock&&wAcc){if(wAx===`h`&&wCar&&wCar._set)wCar._set(wCar._k,!0);else place(0,!0)}wAcc=0;wLock=!1;wPrev=0;wAx=null;wCar=null};
  ov.addEventListener(`wheel`,e=>{if(e.ctrlKey)return;const t=e.target;const k=e.deltaMode===1?40:e.deltaMode===2?H():1,dx=e.deltaX*k,dy=e.deltaY*k;
   const ds=t.closest&&t.closest(`.reel-desc`);if(!wAx&&ds&&ds.scrollHeight>ds.clientHeight+2&&Math.abs(dy)>=Math.abs(dx)){const can=dy>0?ds.scrollTop+ds.clientHeight<ds.scrollHeight-1:ds.scrollTop>0;if(can)return}
   e.preventDefault();const cr=t.closest&&t.closest(`.reel-car`);
   if(!wAx){wAx=cr&&cr._set&&Math.abs(dx)>Math.abs(dy)?`h`:`v`;wCar=wAx===`h`?cr:null}
   const d=wAx===`h`?dx:dy,a=Math.abs(d);
   if(wLock){if(a>wPrev*1.8+8&&a>14){wLock=!1;wAcc=0}else{wPrev=a;clearTimeout(wEndT);wEndT=setTimeout(wEnd,180);return}}
   wPrev=a;wAcc+=d;clearTimeout(wEndT);wEndT=setTimeout(wEnd,180);
   if(wAx===`h`){const N=wCar.querySelectorAll(`.reel-img`).length,edge=(wCar._k===0&&wAcc<0)||(wCar._k===N-1&&wAcc>0);
    if(!edge&&Math.abs(wAcc)>Math.min(90,wCar.clientWidth*.16)){wCar._set(wCar._k+(wAcc>0?1:-1),!0);wAcc=0;wLock=!0;return}wCar._drag&&wCar._drag(-(edge?wAcc*.3:wAcc));return}
   const edge=(i===0&&wAcc<0)||(i===items.length-1&&wAcc>0);
   if(!edge&&Math.abs(wAcc)>Math.min(80,H()*.1)){const dir=wAcc>0?1:-1;wAcc=0;wLock=!0;go(i+dir);return}
   track.style.transition=`none`;place(-(edge?wAcc*.3:wAcc),!1)},{passive:!1});
  '''
c = c[:i] + NEW + c[j:]; print('OK: follow-then-snap wheel')
css = ("@media (min-width: 700px){html.reel-shown .reel{left:50%!important;right:auto!important;width:min(100vw,calc(100vh * 9 / 16))!important;transform:translateX(-50%)}"
       "html.reel-shown .reel.in{transform:translateX(-50%)}html.reel-shown body::before{content:'';position:fixed;inset:0;background:#000;z-index:9499;pointer-events:none}}")
patch("body .lb-ic{", css + "body .lb-ic{", 'phone-shaped column on wide screens')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
