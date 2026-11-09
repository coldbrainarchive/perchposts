#!/usr/bin/env python3
"""Patch v924 -> v925: chirps from other birds that arrive while you're watching "materialize": a glowing
site-purple card the exact size of the new chirp pops into place, the name and message fade in through it,
the purple dissolves and the pinned glow slowly fades (same landing as your own sent chirps). Only for chirps
that arrive live (not the ones already there when a chat opens, not "load older"), only others' chirps, only
when on screen and the tab is visible; skipped for prefers-reduced-motion. Works in any .chat-window (post
chirps, huddles, DMs)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v924.js'
dst = '_deploy/assets/index-DUcNPOLc-v925.js'
content = open(src, encoding='utf-8').read()
JS = r'''
;(()=>{try{
const GLOW='0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)',NOGLOW='0 0 0 0px rgba(192,132,252,0),0 0 0px rgba(192,132,252,0)';
const RM=()=>window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
const mat=(w,body)=>{const br=body.getBoundingClientRect(),wr=w.getBoundingClientRect();
 if(!br.width||br.bottom<wr.top||br.top>wr.bottom)return;
 body.style.opacity='0';const restore=setTimeout(()=>{body.style.opacity=''},1600);
 const RR=(parseFloat(getComputedStyle(body).borderTopLeftRadius)||18)+'px';
 const g=document.createElement('div');
 g.style.cssText='position:fixed;z-index:2147483000;pointer-events:none;box-sizing:border-box;left:'+br.left+'px;top:'+br.top+'px;width:'+br.width+'px;height:'+br.height+'px;border-radius:'+RR+';background:#c084fc;transform-origin:0% 100%;';
 document.body.appendChild(g);
 g.animate([{transform:'scale(.85)',opacity:0,boxShadow:NOGLOW},{transform:'scale(1.03)',opacity:1,boxShadow:GLOW,offset:.6},{transform:'scale(1)',opacity:1,boxShadow:GLOW}],{duration:340,easing:'cubic-bezier(.3,.7,.2,1)',fill:'forwards'}).onfinish=()=>{
  clearTimeout(restore);body.style.opacity='';
  body.animate([{opacity:0},{opacity:0,offset:.15},{opacity:1}],{duration:900,easing:'ease-in-out'});
  g.animate([{opacity:1,background:'rgba(192,132,252,1)',boxShadow:GLOW},{opacity:1,background:'rgba(192,132,252,0.92)',boxShadow:GLOW,offset:.18},{opacity:1,background:'rgba(192,132,252,0)',boxShadow:GLOW,offset:.5},{opacity:1,background:'rgba(192,132,252,0)',boxShadow:NOGLOW}],{duration:2200,easing:'ease-out',fill:'forwards'}).onfinish=()=>g.remove();
 };
};
const seen=new WeakMap();
const scan=()=>{const ws=document.querySelectorAll('.chat-window');if(!ws.length)return;
 ws.forEach(w=>{let st=seen.get(w);const msgs=w.querySelectorAll(':scope > .chat-msg[data-comment-id]');
  if(!st){st={ids:new Set(),t:Date.now()};seen.set(w,st)}
  msgs.forEach((m,idx)=>{const id=m.dataset.commentId;if(st.ids.has(id))return;st.ids.add(id);
   if(Date.now()-st.t<2000||idx>2||m.classList.contains('chat-msg--mine')||document.hidden||RM())return;
   const body=m.querySelector('.chat-msg-body');if(body)mat(w,body)})})};
new MutationObserver(scan).observe(document.body,{childList:true,subtree:true});
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(content + JS); print('Wrote ' + dst)
