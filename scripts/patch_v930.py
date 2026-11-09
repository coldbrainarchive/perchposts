#!/usr/bin/env python3
"""Patch v929 -> v930: fix a scrolling glitch in the chat on Safari mobile.
- v928's Safari scroll-anchoring (needed only on desktop Safari) ran on phones too, reacting to every DOM
  change in the page and nudging scrollTop for ~18 frames, which fought finger/momentum scrolling. It now:
  is off on touch devices (iOS already anchors), only reacts when a chirp is actually added, and never
  nudges within 300ms of the user scrolling/wheeling/touching.
- v926's full-height side panel rule is limited to desktop widths (min-width: 901px)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v929.js'
dst = '_deploy/assets/index-DUcNPOLc-v930.js'
c = open(src, encoding='utf-8').read()
reps = [
 (";(()=>{try{\nconst A=new WeakMap(),bound=new WeakSet(),hold=new WeakMap();",
  ";(()=>{try{\nif(window.matchMedia&&matchMedia('(pointer: coarse)').matches)return;\nconst A=new WeakMap(),bound=new WeakSet(),hold=new WeakMap(),lastUser=new WeakMap();\nconst added=ms=>ms.some(m=>[...m.addedNodes].some(n=>n.nodeType===1&&(n.matches&&n.matches('.chat-msg')||n.querySelector&&n.querySelector('.chat-msg'))));"),
 ("const fix=()=>{const ws=document.querySelectorAll('.chat-window');if(!ws.length)return;",
  "const fix=ms=>{const ws=document.querySelectorAll('.chat-window');if(!ws.length)return;const chirp=added(ms||[]);"),
 ("['wheel','touchstart','keydown'].forEach(ev=>w.addEventListener(ev,()=>{hold.set(w,0)},{passive:true}));rec(w);return}",
  "['wheel','touchstart','keydown','mousedown'].forEach(ev=>w.addEventListener(ev,()=>{hold.set(w,0);lastUser.set(w,Date.now())},{passive:true}));rec(w);return}\n  if(!chirp||Date.now()-(lastUser.get(w)||0)<300){rec(w);return}"),
 (".comments-shell:not(.chat-preview):not(.chat-full){height:calc(100dvh - 91px)}",
  "@media (min-width: 901px){.comments-shell:not(.chat-preview):not(.chat-full){height:calc(100dvh - 91px)}}"),
]
for o, n in reps:
    if c.count(o) != 1: print('FAIL', c.count(o), o[:70]); sys.exit(1)
    c = c.replace(o, n)
open(dst, 'w', encoding='utf-8').write(c); print('Wrote ' + dst)
