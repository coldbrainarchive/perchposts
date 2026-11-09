#!/usr/bin/env python3
"""Patch v917 -> v918: sending a chirp launches your own bird (its emoji, colour filter and sparkles, cloned
from the header pill) from the send button up to where the chirp lands. It flaps (quick squash/stretch)
along a small arc; as it arrives the chirp bubble pops in (hidden while the bird flies, even if the server's
copy replaces the instant one mid-flight) and a couple of feathers drift off. ~0.6s. Skipped for
prefers-reduced-motion."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v917.js'
dst = '_deploy/assets/index-DUcNPOLc-v918.js'
content = open(src, encoding='utf-8').read()
old = 'is_admin:s.is_admin,isPending:!0}]);'
if content.count(old) != 1: print('FAIL hook', content.count(old)); sys.exit(1)
content = content.replace(old, old + 'window._chirpFly&&window._chirpFly(a);')
JS = r'''
;(()=>{try{
const st=document.createElement('style');
st.textContent='.chirp-fly .chat-window > .chat-msg:nth-child(1 of .chat-msg--mine) .chat-msg-body{opacity:0!important;transform:scale(.6);transform-origin:100% 100%}';
document.head.appendChild(st);
window._chirpFly=function(id){try{
 if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 const src=(document.querySelector('.chat-send-btn')||document.querySelector('.chat-compose'));if(!src)return;
 const fr=src.getBoundingClientRect();
 const badge=document.querySelector('.nav-user-pill .user-pill-badge');
 document.documentElement.classList.add('chirp-fly');
 const newest=()=>{const w=document.querySelector('.chat-window');return w&&(w.querySelector('.chat-msg[data-comment-id="'+id+'"] .chat-msg-body')||w.querySelector(':scope > .chat-msg:nth-child(1 of .chat-msg--mine) .chat-msg-body'))};
 requestAnimationFrame(()=>requestAnimationFrame(()=>{
  const b=newest();const tr=b?b.getBoundingClientRect():{left:fr.left-60,right:fr.left-20,top:fr.top-140,height:30};
  const x0=fr.left+fr.width/2,y0=fr.top+fr.height/2,x1=Math.min(tr.right-18,innerWidth-24),y1=tr.top+Math.min(tr.height,60)/2;
  const xm=(x0+x1)/2-50,ym=Math.min(y0,y1)-50;
  const bird=document.createElement('div');
  bird.style.cssText='position:fixed;left:0;top:0;z-index:2147483000;pointer-events:none;will-change:transform,opacity;';
  const flap=document.createElement('div');flap.style.cssText='display:flex;align-items:center;justify-content:center;width:30px;height:30px;margin:-15px 0 0 -15px;font-size:26px;line-height:1;transform-origin:50% 60%;';
  let face;if(badge){face=badge.cloneNode(true);face.style.cssText='position:relative;display:inline-flex;align-items:center;justify-content:center;font-size:26px;width:30px;height:30px;line-height:1;';face.querySelectorAll('img').forEach(i=>{i.style.width='28px';i.style.height='28px'})}
  else{face=document.createElement('span');face.textContent='🐦'}
  flap.appendChild(face);bird.appendChild(flap);document.body.appendChild(bird);
  flap.animate([{transform:'scaleY(1) rotate(-10deg)'},{transform:'scaleY(.55) scaleX(1.12) rotate(6deg)'},{transform:'scaleY(1) rotate(-10deg)'}],{duration:150,iterations:Infinity});
  const tf=(x,y,s)=>'translate('+x+'px,'+y+'px) scale('+s+')';
  const fly=bird.animate([{transform:tf(x0,y0,.5),opacity:0},{transform:tf((x0+xm)/2,(y0+ym)/2+10,.95),opacity:1,offset:.25},{transform:tf(xm,ym,1.15),opacity:1,offset:.55},{transform:tf(x1,y1,.9),opacity:1}],{duration:560,easing:'cubic-bezier(.35,.1,.35,1)',fill:'forwards'});
  let done=false;const land=()=>{if(done)return;done=true;
   document.documentElement.classList.remove('chirp-fly');
   const nb=newest();if(nb){nb.style.transformOrigin='100% 100%';nb.animate([{opacity:0,transform:'scale(.6)'},{opacity:1,transform:'scale(1.07)',offset:.6},{opacity:1,transform:'scale(1)'}],{duration:300,easing:'ease-out'})}
   bird.animate([{transform:tf(x1,y1,.9),opacity:1},{transform:tf(x1+22,y1-34,.45),opacity:0}],{duration:320,easing:'ease-in',fill:'forwards'}).onfinish=()=>bird.remove();
   for(let k=0;k<3;k++){const f=document.createElement('div');f.textContent='🪶';f.style.cssText='position:fixed;left:0;top:0;z-index:2147483000;pointer-events:none;font-size:'+(11+k*2)+'px;';document.body.appendChild(f);
    const dx=(k-1)*26+(Math.random()*10-5),dy=26+Math.random()*18,r=(k-1)*70+(Math.random()*40-20);
    f.animate([{transform:'translate('+x1+'px,'+y1+'px) rotate(0deg)',opacity:.95},{transform:'translate('+(x1+dx)+'px,'+(y1+dy)+'px) rotate('+r+'deg)',opacity:0}],{duration:700+k*120,easing:'cubic-bezier(.2,.6,.4,1)',fill:'forwards'}).onfinish=()=>f.remove()}
  };
  fly.onfinish=land;setTimeout(land,900);
 }));
 setTimeout(()=>document.documentElement.classList.remove('chirp-fly'),1500);
}catch(e){document.documentElement.classList.remove('chirp-fly')}};
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(content + JS); print('Wrote ' + dst)
