#!/usr/bin/env python3
"""Patch v920 -> v921: the flying chirp no longer goes square before rounding again. It was easing toward the
bubble's own corner radius, which is 0 (the rounding comes from the chirp body clipping at 18px). The pill
now lands with the body's 18px corners (a pill at bubble height), and as the name header grows out of the
top, the real bubble's top corners straighten from 18px to square to meet it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v920.js'
dst = '_deploy/assets/index-DUcNPOLc-v921.js'
content = open(src, encoding='utf-8').read()
reps = [
 ("const tr=bub.getBoundingClientRect(),cs=getComputedStyle(bub);",
  "const tr=bub.getBoundingClientRect(),cs=getComputedStyle(bub),RR=(parseFloat(getComputedStyle(body).borderTopLeftRadius)||18)+'px';"),
 ("borderRadius:cs.borderRadius,background:'#7c3aed',fontSize:cs.fontSize", "borderRadius:RR,background:'#7c3aed',fontSize:cs.fontSize"),
 ("if(b2){const to=getComputedStyle(b2).backgroundColor;",
  "if(b2&&mt){const RR2=(parseFloat(getComputedStyle(nb).borderTopLeftRadius)||18)+'px';b2.animate([{borderTopLeftRadius:RR2,borderTopRightRadius:RR2},{borderTopLeftRadius:'0px',borderTopRightRadius:'0px'}],{duration:320,easing:'cubic-bezier(.3,.7,.2,1)'})}\n"
  "   if(b2){const to=getComputedStyle(b2).backgroundColor;"),
]
for o, n in reps:
    if content.count(o) != 1: print('FAIL', content.count(o), o[:60]); sys.exit(1)
    content = content.replace(o, n)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
