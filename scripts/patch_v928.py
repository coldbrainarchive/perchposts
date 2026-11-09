#!/usr/bin/env python3
"""Patch v927 -> v928: desktop Safari no longer jumps the chirp you're reading when a new chirp arrives
while you're scrolled up. Safari has no CSS scroll anchoring, so in the bottom-up (column-reverse) chat a new
chirp at the bottom pushed everything up by its height (measured in real Safari 26: -80px). While you're
scrolled up, the chirp you're looking at and its position are remembered; after any change to the chat
(before the screen repaints) the scroll is nudged so it stays exactly where it was, and held there for ~18 frames (Safari sometimes shifts it again a moment later). Scrolling/touching cancels the hold. A no-op in browsers that
already anchor (Chrome, iOS), and when you're at the bottom (new chirps keep following)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v927.js'
dst = '_deploy/assets/index-DUcNPOLc-v928.js'
content = open(src, encoding='utf-8').read()
JS = r'''
;(()=>{try{
const A=new WeakMap(),bound=new WeakSet(),hold=new WeakMap();
const pick=w=>{const wr=w.getBoundingClientRect();for(const m of w.querySelectorAll(':scope > .chat-msg')){const r=m.getBoundingClientRect();if(r.bottom>wr.top+4&&r.top<wr.bottom-4)return m}return null};
const rec=w=>{if(hold.get(w))return;if(Math.abs(w.scrollTop)<=60){A.set(w,null);return}const m=pick(w);A.set(w,m?{el:m,top:m.getBoundingClientRect().top}:null)};
const keep=(w,a)=>{const d=a.el.getBoundingClientRect().top-a.top;if(Math.abs(d)>=1)w.scrollTop+=d};
const fix=()=>{const ws=document.querySelectorAll('.chat-window');if(!ws.length)return;
 ws.forEach(w=>{if(!bound.has(w)){bound.add(w);w.addEventListener('scroll',()=>rec(w),{passive:true});['wheel','touchstart','keydown'].forEach(ev=>w.addEventListener(ev,()=>{hold.set(w,0)},{passive:true}));rec(w);return}
  const a=A.get(w);if(!a||!a.el.isConnected){rec(w);return}
  keep(w,a);
  // hold the chirp you're reading in place for a few frames: Safari can shift it again after the change
  const id=(hold.get(w)||0)+1;hold.set(w,id);let f=0;
  const tick=()=>{if(hold.get(w)!==id)return;if(a.el.isConnected)keep(w,a);if(++f<18)requestAnimationFrame(tick);else{hold.set(w,0);rec(w)}};
  requestAnimationFrame(tick)})};
new MutationObserver(fix).observe(document.body,{childList:true,subtree:true});
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(content + JS); print('Wrote ' + dst)
