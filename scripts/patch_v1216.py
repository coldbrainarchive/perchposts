#!/usr/bin/env python3
"""Patch v1215 -> v1216: the scroller works with a mouse / trackpad on computers.
- Mouse wheel / two-finger trackpad scroll: one post per gesture (momentum doesn't skip posts); sideways scroll on a
  photo set moves one photo; long text still scrolls itself first.
- Click-and-drag like a phone swipe: drag up / down to change post, left / right on a photo set; a drag doesn't
  count as a click on whatever it ends over. Grab cursor.
- The first-post hint on computers says "Scroll or drag up for the next post"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1215.js'
dst = '_deploy/assets/index-DUcNPOLc-v1216.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
DESK = r'''ov.addEventListener(`click`,e=>{if(moved){moved=!1;return}});
 {let wAcc=0,wT=0,wLock=0;ov.addEventListener(`wheel`,e=>{if(e.ctrlKey)return;const t=e.target;const ds=t.closest&&t.closest(`.reel-desc`);
   if(ds&&ds.scrollHeight>ds.clientHeight+2&&Math.abs(e.deltaY)>=Math.abs(e.deltaX)){const can=e.deltaY>0?ds.scrollTop+ds.clientHeight<ds.scrollHeight-1:ds.scrollTop>0;if(can)return}
   e.preventDefault();const now=Date.now();if(now<wLock){wLock=Math.max(wLock,now+140);return}if(now-wT>220)wAcc=0;wT=now;
   const cr=t.closest&&t.closest(`.reel-car`);if(cr&&cr._set&&Math.abs(e.deltaX)>Math.abs(e.deltaY)){wAcc+=e.deltaX;if(Math.abs(wAcc)>40){cr._set(cr._k+(wAcc>0?1:-1),!0);wAcc=0;wLock=now+450}return}
   if(Math.abs(e.deltaY)<Math.abs(e.deltaX))return;wAcc+=e.deltaY;if(Math.abs(wAcc)>40){go(i+(wAcc>0?1:-1));wAcc=0;wLock=now+550}},{passive:!1});
  let md=null;ov.addEventListener(`dragstart`,e=>e.preventDefault());
  ov.addEventListener(`pointerdown`,e=>{if(e.pointerType!==`mouse`||e.button!==0)return;const t=e.target;if(t.closest&&t.closest(`button,a,input,textarea,.reel-panel,.reel-x,.reel-gct,.reel-gmu,.reel-desc`))return;
   md={x:e.clientX,y:e.clientY,t:Date.now(),ax:null,car:t.closest&&t.closest(`.reel-car`),dx:0,dy:0,id:e.pointerId};track.style.transition=`none`});
  ov.addEventListener(`pointermove`,e=>{if(!md||e.pointerId!==md.id)return;md.dx=e.clientX-md.x;md.dy=e.clientY-md.y;
   if(!md.ax&&Math.hypot(md.dx,md.dy)>8){md.ax=Math.abs(md.dy)>Math.abs(md.dx)?`v`:`h`;try{ov.setPointerCapture(md.id)}catch(_){}ov.classList.add(`reel-dragging`)}
   if(md.ax===`v`){const edge=(i===0&&md.dy>0)||(i===items.length-1&&md.dy<0);place(edge?md.dy*.3:md.dy,!1)}else if(md.ax===`h`&&md.car&&md.car._drag)md.car._drag(md.dx)});
  const mEnd=e=>{if(!md)return;const d=md;md=null;ov.classList.remove(`reel-dragging`);if(!d.ax){place(0,!0);return}ov._dragT=Date.now();const dt=Math.max(1,Date.now()-d.t);
   if(d.ax===`v`){const fast=Math.abs(d.dy)>30&&Math.abs(d.dy)/dt>.45;if(Math.abs(d.dy)>H()*.18||fast)go(i+(d.dy<0?1:-1));else place(0,!0)}
   else{if(d.car&&d.car._set){const fast=Math.abs(d.dx)>30&&Math.abs(d.dx)/dt>.45;d.car._set(d.car._k+((Math.abs(d.dx)>d.car.clientWidth*.2||fast)?(d.dx<0?1:-1):0),!0)}place(0,!0)}};
  ov.addEventListener(`pointerup`,mEnd);ov.addEventListener(`pointercancel`,mEnd);
  ov.addEventListener(`click`,e=>{if(Date.now()-(ov._dragT||0)<300){e.preventDefault();e.stopPropagation()}},!0)}'''
patch("ov.addEventListener(`click`,e=>{if(moved){moved=!1;return}});", DESK, 'wheel + mouse drag')
patch(":last&&loading?`Loading more…`:`Swipe up for the next post`;",
      ":last&&loading?`Loading more…`:(matchMedia(`(hover: hover) and (pointer: fine)`).matches?`Scroll or drag up for the next post`:`Swipe up for the next post`);", 'desktop hint wording')
patch("body .lb-ic{", "@media (hover: hover) and (pointer: fine){body .reel-view{cursor:grab}body .reel.reel-dragging,body .reel.reel-dragging *{cursor:grabbing!important}}body .lb-ic{", 'grab cursor')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
