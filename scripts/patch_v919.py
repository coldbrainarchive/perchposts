#!/usr/bin/env python3
"""Patch v917 -> v919 (replaces v918's bird flight): sending a chirp lifts the typed message out of the
compose box and glides it straight to its spot in the chirp chat. On the way it reshapes from the compose
pill into a chat bubble and turns purple; on landing the real chirp takes its place, glowing purple, and the
purple slowly fades back to the normal bubble colour (~1.4s). The real chirp stays hidden in flight (even if
the server's copy replaces the instant one). Skipped for prefers-reduced-motion."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v917.js'
dst = '_deploy/assets/index-DUcNPOLc-v919.js'
content = open(src, encoding='utf-8').read()
old = 'is_admin:s.is_admin,isPending:!0}]);'
if content.count(old) != 1: print('FAIL hook', content.count(old)); sys.exit(1)
content = content.replace(old, old + 'window._chirpFly&&window._chirpFly(a,t);')
JS = r'''
;(()=>{try{
const st=document.createElement('style');
st.textContent='.chirp-fly .chat-window > .chat-msg:nth-child(1 of .chat-msg--mine) .chat-msg-body{opacity:0!important}';
document.head.appendChild(st);
const H=document.documentElement;
window._chirpFly=function(id,text){try{
 if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 const cb=document.querySelector('.chat-compose .chat-input-bubble');if(!cb)return;
 const fr=cb.getBoundingClientRect();
 H.classList.add('chirp-fly');
 const done=()=>H.classList.remove('chirp-fly');setTimeout(done,1600);
 const newest=()=>{const w=document.querySelector('.chat-window');return w&&(w.querySelector('.chat-msg[data-comment-id="'+id+'"] .chat-msg-body')||w.querySelector(':scope > .chat-msg:nth-child(1 of .chat-msg--mine) .chat-msg-body'))};
 requestAnimationFrame(()=>requestAnimationFrame(()=>{
  const body=newest();const bub=body&&(body.querySelector('.chat-bubble')||body);
  if(!bub){done();return}
  const tr=bub.getBoundingClientRect(),cs=getComputedStyle(bub);
  const g=document.createElement('div');
  g.textContent=(text||'').slice(0,400);
  g.style.cssText='position:fixed;z-index:2147483000;pointer-events:none;box-sizing:border-box;overflow:hidden;white-space:pre-wrap;word-break:break-word;'+
   'color:#f8fafc;line-height:1.4;font-family:inherit;border:1px solid rgba(255,255,255,0.07);';
  document.body.appendChild(g);
  const px=v=>Math.round(v)+'px';
  const a=g.animate([
   {left:px(fr.left),top:px(fr.top),width:px(fr.width),height:px(fr.height),borderRadius:'28px',background:'#0d0f14',fontSize:'16px',padding:'12px 16px',borderColor:'rgba(255,255,255,0.07)',boxShadow:'0 0 0 rgba(192,132,252,0)'},
   {offset:.4,background:'#7c3aed',borderColor:'#7c3aed',boxShadow:'0 0 18px rgba(192,132,252,.6)'},
   {left:px(tr.left),top:px(tr.top),width:px(tr.width),height:px(tr.height),borderRadius:cs.borderRadius,background:'#7c3aed',fontSize:cs.fontSize,padding:cs.padding,borderColor:'#7c3aed',boxShadow:'0 0 18px rgba(192,132,252,.6)'}
  ],{duration:480,easing:'cubic-bezier(.3,.7,.2,1)',fill:'forwards'});
  let landed=false;const land=()=>{if(landed)return;landed=true;
   done();
   const nb=newest();const b2=nb&&(nb.querySelector('.chat-bubble')||nb);
   if(nb)nb.animate([{opacity:0},{opacity:1}],{duration:140,easing:'ease-out'});
   if(b2){const to=getComputedStyle(b2).backgroundColor;b2.animate([{background:'#7c3aed',boxShadow:'0 0 18px rgba(192,132,252,.6)'},{background:'#7c3aed',boxShadow:'0 0 14px rgba(192,132,252,.45)',offset:.25},{background:to,boxShadow:'0 0 0 rgba(192,132,252,0)'}],{duration:1400,easing:'ease-out'})}
   g.animate([{opacity:1},{opacity:0}],{duration:160,easing:'ease-out',fill:'forwards'}).onfinish=()=>g.remove();
  };
  a.onfinish=land;setTimeout(land,800);
 }));
}catch(e){H.classList.remove('chirp-fly')}};
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(content + JS); print('Wrote ' + dst)
