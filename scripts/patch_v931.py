#!/usr/bin/env python3
"""ROLLED BACK (user preferred v930; real cause was the timestamp). Patch v930 -> v931: no more one-frame jump when a chirp arrives (seen in the user's iPhone recording at
6.33s -> 6.40s: every chirp above jumped up a whole chirp's height in one frame while the new one appeared).
When a new chirp is added at the bottom while you're at the bottom, the older chirps now glide up into place
(~0.26s) while the new chirp materializes / your sent chirp lands in the space. Only when the previous
newest chirp really moved (so swapping your instant chirp for the server's copy doesn't fake a glide);
skipped for prefers-reduced-motion and when scrolled up (then you get the "new chirps" pill)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v930.js'
dst = '_deploy/assets/index-DUcNPOLc-v931.js'
c = open(src, encoding='utf-8').read()
old = ("  msgs.forEach((m,idx)=>{const id=m.dataset.commentId;if(st.ids.has(id))return;st.ids.add(id);\n"
       "   if(Date.now()-st.t<2000||idx>2||m.classList.contains('chat-msg--mine'))return;\n"
       "   if(Math.abs(w.scrollTop)>60){st.unread=(st.unread||0)+1;pill(w,st);return}\n"
       "   if(document.hidden||RM())return;\n"
       "   const body=m.querySelector('.chat-msg-body');if(body)mat(w,body)})})};")
new = ("  let glided=false;\n"
       "  msgs.forEach((m,idx)=>{const id=m.dataset.commentId;if(st.ids.has(id))return;st.ids.add(id);\n"
       "   if(Date.now()-st.t<2000||idx>2)return;\n"
       "   const atBottom=Math.abs(w.scrollTop)<=60;\n"
       "   if(atBottom&&!glided&&st.top&&!RM()&&!document.hidden){const prev=w.querySelector(':scope > .chat-msg[data-comment-id=\"'+st.top.id+'\"]');\n"
       "    if(prev&&prev!==m){const dy=st.top.off-prev.offsetTop;if(dy>2){glided=true;glide(w,m,dy)}}}\n"
       "   if(m.classList.contains('chat-msg--mine'))return;\n"
       "   if(!atBottom){st.unread=(st.unread||0)+1;pill(w,st);return}\n"
       "   if(document.hidden||RM())return;\n"
       "   const body=m.querySelector('.chat-msg-body');if(body)mat(w,body)});\n"
       "  if(msgs[0])st.top={id:msgs[0].dataset.commentId,off:msgs[0].offsetTop}})};")
if c.count(old) != 1: print('FAIL scan', c.count(old)); sys.exit(1)
c = c.replace(old, new)
old2 = "const seen=new WeakMap();"
new2 = ("const glide=(w,m,dy)=>{const wr=w.getBoundingClientRect();let n=0;\n"
        " for(let el=m.nextElementSibling;el&&n<30;el=el.nextElementSibling,n++){const r=el.getBoundingClientRect();if(r.bottom<wr.top-dy-10)break;\n"
        "  el.animate([{transform:'translateY('+dy+'px)'},{transform:'translateY(0px)'}],{duration:260,easing:'cubic-bezier(.3,.7,.2,1)'})}};\n"
        "const seen=new WeakMap();")
if c.count(old2) != 1: print('FAIL seen', c.count(old2)); sys.exit(1)
c = c.replace(old2, new2)
open(dst, 'w', encoding='utf-8').write(c); print('Wrote ' + dst)
