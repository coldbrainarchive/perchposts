#!/usr/bin/env python3
"""Patch v1302 -> v1303: the Share sheet's top handle closes it: tap it, or drag it down (follows the finger;
past 70px or a quick flick closes, otherwise it springs back). Hit area is the full width of the sheet's top."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1302.js'
dst = '_deploy/assets/index-DUcNPOLc-v1303.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const bye=()=>{setIn(!1);setTimeout(close,240)};",
      "const bye=()=>{setIn(!1);setTimeout(close,240)};const dg=(0,_.useRef)(null);"
      "const shOf=ev=>ev.currentTarget.closest(`.ps-sheet`);"
      "const dS=ev=>{const sh=shOf(ev);if(!sh)return;try{document.activeElement&&document.activeElement.blur()}catch(e){}dg.current={y:ev.touches[0].clientY,t:Date.now(),dy:0};sh.style.transition=`none`};"
      "const dM=ev=>{const d=dg.current,sh=shOf(ev);if(!d||!sh)return;d.dy=Math.max(0,ev.touches[0].clientY-d.y);sh.style.transform=`translateY(${d.dy}px)`};"
      "const dE=ev=>{const d=dg.current,sh=shOf(ev);dg.current=null;if(!d||!sh)return;sh.style.transition=``;const v=d.dy/Math.max(1,Date.now()-d.t);"
      "if(d.dy>70||(d.dy>18&&v>.5)){sh.style.transform=`translateY(100%)`;bye()}else{sh.style.transform=``}};", 'drag handlers')
patch("children:[(0,L.jsx)(`div`,{className:`ps-grab`}),\n  (0,L.jsx)(`div`,{className:`ps-lbl`,children:`Send to a huddle`}),",
      "children:[(0,L.jsx)(`div`,{className:`ps-grabz`,role:`button`,\"aria-label\":`Close`,onClick:bye,onTouchStart:dS,onTouchMove:dM,onTouchEnd:dE,onTouchCancel:dE,children:(0,L.jsx)(`div`,{className:`ps-grab`})}),\n  (0,L.jsx)(`div`,{className:`ps-lbl`,children:`Send to a huddle`}),", 'handle')
patch("body .ps-grab{", "body .ps-grabz{margin:-8px -20px 2px;padding:10px 20px 14px;touch-action:none;cursor:pointer;-webkit-tap-highlight-color:transparent}body .ps-grabz .ps-grab{margin:0 auto}body .ps-grab{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
