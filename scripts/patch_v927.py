#!/usr/bin/env python3
"""Patch v926 -> v927: "↓ N new chirps" pill. When chirps from others arrive while you're scrolled up in a chat
(more than ~60px from the newest), a site-purple pill appears just above the compose box with the count.
Tapping it glides to the newest chirp; it disappears once you're back at the bottom (by tap or scrolling).
(At the bottom, new chirps keep following as before, like iMessage / WhatsApp.)"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v926.js'
dst = '_deploy/assets/index-DUcNPOLc-v927.js'
content = open(src, encoding='utf-8').read()
old = "   if(Date.now()-st.t<2000||idx>2||m.classList.contains('chat-msg--mine')||document.hidden||RM())return;"
new = ("   if(Date.now()-st.t<2000||idx>2||m.classList.contains('chat-msg--mine'))return;\n"
       "   if(Math.abs(w.scrollTop)>60){st.unread=(st.unread||0)+1;pill(w,st);return}\n"
       "   if(document.hidden||RM())return;")
if content.count(old) != 1: print('FAIL hook', content.count(old)); sys.exit(1)
content = content.replace(old, new)
old2 = "const seen=new WeakMap();"
new2 = r'''const pill=(w,st)=>{let p=st.pill;
 if(!p){p=document.createElement('button');p.type='button';
  p.style.cssText='position:fixed;z-index:2147482000;transform:translateX(-50%);display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 14px;border-radius:999px;border:1px solid #c084fc;background:#c084fc;color:#14081d;font-size:12px;font-weight:800;line-height:1;font-family:inherit;cursor:pointer;box-shadow:0 0 0 3px rgba(192,132,252,0.35),0 4px 16px rgba(0,0,0,0.45);white-space:nowrap;';
  p.onclick=()=>{w.scrollTo({top:0,behavior:RM()?'auto':'smooth'})};
  document.body.appendChild(p);st.pill=p;
  const place=()=>{if(!w.isConnected){p.remove();st.pill=null;return}const r=w.getBoundingClientRect();p.style.left=(r.left+r.width/2)+'px';p.style.top=(r.bottom-40)+'px'};
  st.place=place;
  if(!st.bound){st.bound=1;w.addEventListener('scroll',()=>{if(Math.abs(w.scrollTop)<=60&&st.pill){st.unread=0;const q=st.pill;st.pill=null;q.animate([{opacity:1},{opacity:0,transform:'translateX(-50%) translateY(6px)'}],{duration:180,fill:'forwards'}).onfinish=()=>q.remove()}else if(st.place)st.place()},{passive:true});
  addEventListener('resize',()=>st.place&&st.place());}
  p.animate([{opacity:0,transform:'translateX(-50%) translateY(8px) scale(.9)'},{opacity:1,transform:'translateX(-50%) translateY(0) scale(1)'}],{duration:220,easing:'cubic-bezier(.3,.7,.2,1)'});
 }
 st.place&&st.place();p.textContent='↓ '+st.unread+' new chirp'+(st.unread===1?'':'s');
};
const seen=new WeakMap();'''
if content.count(old2) != 1: print('FAIL seen', content.count(old2)); sys.exit(1)
content = content.replace(old2, new2)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
