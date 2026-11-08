#!/usr/bin/env python3
"""Patch v875 -> v876: temporary readout for the iPhone search-bar bug, on top of v875's fix (which didn't cure it).
Same readout as v874 (on with /?vvdebug=1) but without v874's invisible 100dvh/svh/lvh measuring boxes, which made
the page longer and seemed to hide the bug. Also shows page height, max scroll, and whether v875's extra space
is showing. Remove once the cause is found.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v875.js'
dst = '_deploy/assets/index-DUcNPOLc-v876.js'
content = open(src, encoding='utf-8').read()

old = "document.body.appendChild(room);"
if content.count(old) != 1:
    print('FAIL: room anchor'); sys.exit(1)
content = content.replace(old, old + "window.__ppRoom=room;")

READOUT = r'''
;(()=>{try{
const q=new URLSearchParams(location.search).get('vvdebug');
if(q==='1')localStorage.setItem('vvdebug','1');
if(q==='0')localStorage.removeItem('vvdebug');
if(localStorage.getItem('vvdebug')!=='1')return;
const box=document.createElement('div');
box.style.cssText='position:fixed;left:8px;right:8px;top:0;z-index:2147483647;background:rgba(0,0,0,.88);color:#7CFC9A;font:11px/1.35 ui-monospace,Menlo,monospace;padding:6px 8px;border-radius:8px;border:1px solid #7CFC9A;pointer-events:none;white-space:pre;';
document.body.appendChild(box);
const vv=window.visualViewport;
const r=s=>{const e=document.querySelector(s);if(!e)return'-';const b=e.getBoundingClientRect();return Math.round(b.top)+'..'+Math.round(b.bottom)};
const st={tapY:null,focusY:null,maxOff:0,maxDY:0,log:[]};
const ov=()=>{const h=getComputedStyle(document.documentElement),b=getComputedStyle(document.body);return 'html '+h.overflowY+'/'+h.position+' body '+b.overflowY+'/'+b.position};
const draw=()=>{
 const off=vv?vv.offsetTop:0,vh=vv?vv.height:innerHeight;
 if(off>st.maxOff)st.maxOff=off;
 if(st.focusY!==null){const d=Math.abs(scrollY-st.focusY);if(d>st.maxDY)st.maxDY=d}
 box.style.transform='translateY('+Math.round(off+vh-box.offsetHeight-8)+'px)';
 box.textContent=
  'scrollY '+Math.round(scrollY)+'  tapY '+st.tapY+'  focusY '+st.focusY+'  maxDY '+Math.round(st.maxDY)+'\n'+
  'innerH '+innerHeight+'  vv.off '+Math.round(off)+'  vv.h '+Math.round(vh)+'  maxOff '+Math.round(st.maxOff)+'\n'+
  'topbar '+r('.app-topbar')+'  shell '+r('.search-shell')+'  panel '+r('.search-columns')+'\n'+
  'active '+((document.activeElement&&document.activeElement.className)||'-').toString().slice(0,20)+'  '+ov()+'\n'+
  'docH '+document.documentElement.scrollHeight+'  maxY '+(document.documentElement.scrollHeight-innerHeight)+'  room '+(window.__ppRoom?window.__ppRoom.style.display:'?')+'\n'+
  st.log.slice(-5).join('\n');
};
const meas=()=>{};
document.addEventListener('touchstart',e=>{if(e.target.closest&&e.target.closest('.search-input')){st.tapY=Math.round(scrollY);st.maxOff=0;st.maxDY=0;st.log=[]}},{passive:true,capture:true});
document.addEventListener('focusin',e=>{if(e.target.classList&&e.target.classList.contains('search-input')){st.focusY=Math.round(scrollY);const t0=performance.now();
 [100,300,600,1000,1500].forEach(ms=>setTimeout(()=>{st.log.push(ms+'ms y'+Math.round(scrollY)+' off'+Math.round(vv?vv.offsetTop:0)+' vh'+Math.round(vv?vv.height:0)+' ih'+innerHeight+' shell'+r('.search-shell'));draw()},ms))}},true);
const tick=()=>{meas();draw()};
if(vv){vv.addEventListener('resize',tick);vv.addEventListener('scroll',tick)}
addEventListener('scroll',tick,{passive:true});
setInterval(tick,250);tick();
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(content + READOUT)
print('Wrote ' + dst)
