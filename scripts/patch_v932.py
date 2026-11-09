#!/usr/bin/env python3
"""Patch v930 -> v932 (v931's glide was rolled back): an incoming chirp's space opens smoothly before it
appears. When another bird's chirp arrives while you're at the bottom, its row grows from 0 to full height
(~0.26s, the 6px gap too), gently pushing the older chirps up; once the room is made, the chirp
materializes into it. Fixes the one-frame jump seen in the user's iPhone recording (everything jumped up a
chirp's height as the new one was placed at full size at once)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v930.js'
dst = '_deploy/assets/index-DUcNPOLc-v932.js'
c = open(src, encoding='utf-8').read()
old = "   if(document.hidden||RM())return;\n   const body=m.querySelector('.chat-msg-body');if(body)mat(w,body)})})};"
new = ("   if(document.hidden||RM())return;\n"
       "   const body=m.querySelector('.chat-msg-body');if(!body)return;\n"
       "   if(idx===0)openGap(m,body,()=>mat(w,body));else mat(w,body)})})};")
if c.count(old) != 1: print('FAIL scan', c.count(old)); sys.exit(1)
c = c.replace(old, new)
old2 = "const seen=new WeakMap();"
new2 = ("const openGap=(m,body,done)=>{const H=m.offsetHeight;if(!H){done();return}\n"
        " body.style.opacity='0';const safe=setTimeout(()=>{body.style.opacity='';m.style.overflow=''},2500);\n"
        " m.style.overflow='hidden';\n"
        " const a=m.animate([{height:'0px',marginTop:'-6px'},{height:H+'px',marginTop:'0px'}],{duration:260,easing:'cubic-bezier(.3,.7,.2,1)'});\n"
        " a.onfinish=a.oncancel=()=>{clearTimeout(safe);m.style.overflow='';done()}};\n"
        "const seen=new WeakMap();")
if c.count(old2) != 1: print('FAIL seen', c.count(old2)); sys.exit(1)
c = c.replace(old2, new2)
open(dst, 'w', encoding='utf-8').write(c); print('Wrote ' + dst)
