#!/usr/bin/env python3
"""Patch v906 -> v907: the sliding toggle pill left a hairline gap at the end (seen on POST | HUDDLE).
offsetLeft/offsetWidth round to whole pixels; the pill is now placed with exact (fractional) left/right
offsets, and tucked 1px under the outline (-1, the toggle stops clipping once the pill is placed, so at the ends the pill covers the outline and its curve is the outline's outer curve) at the ends so no seam shows when the first or last option is active."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v906.js'
dst = '_deploy/assets/index-DUcNPOLc-v907.js'
content = open(src, encoding='utf-8').read()
reps = [
 (" const l=a.offsetLeft+'px',w=a.offsetWidth+'px';if(th.style.left===l&&th.style.width===w&&el.classList.contains('tg-ready'))return;\n"
  " if(!anim||!el.classList.contains('tg-ready')){th.style.transition='none';th.style.left=l;th.style.width=w;void th.offsetWidth;th.style.transition='';el.classList.add('tg-ready')}\n"
  " else{th.style.left=l;th.style.width=w}};",
  " const bs=[...el.querySelectorAll(':scope > button')],er=el.getBoundingClientRect(),ar=a.getBoundingClientRect(),inner=er.width-el.clientLeft*2;\n"
  " const L0=a===bs[0]?-1:ar.left-er.left-el.clientLeft,R0=a===bs[bs.length-1]?-1:inner-(ar.right-er.left-el.clientLeft);\n"
  " const l=L0.toFixed(2)+'px',w=Math.max(-1,R0).toFixed(2)+'px';if(th.style.left===l&&th.style.right===w&&el.classList.contains('tg-ready'))return;\n"
  " if(!anim||!el.classList.contains('tg-ready')){th.style.transition='none';th.style.left=l;th.style.right=w;void th.offsetWidth;th.style.transition='';el.classList.add('tg-ready')}\n"
  " else{th.style.left=l;th.style.right=w}};"),
 (".tg-thumb { position: absolute; top: 0; bottom: 0; left: 0; width: 0;", ".tg-thumb { position: absolute; top: -1px; bottom: -1px; left: 0; right: 100%;"),
 (".tg-ready > button { position: relative; z-index: 1; }", ".tg-ready { overflow: visible !important; }\n      .tg-ready > button { position: relative; z-index: 1; }"),
 ("transition: left 0.25s cubic-bezier(.3,.7,.3,1), width 0.25s cubic-bezier(.3,.7,.3,1);", "transition: left 0.25s cubic-bezier(.3,.7,.3,1), right 0.25s cubic-bezier(.3,.7,.3,1);"),
]
for o, n in reps:
    if content.count(o) != 1: print('FAIL', content.count(o), o[:70]); sys.exit(1)
    content = content.replace(o, n)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
