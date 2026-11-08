#!/usr/bin/env python3
"""Patch v873 -> v874: temporary viewport readout for the iPhone search-bar bug (header and search bar vanish
above the screen when the search bar is tapped while scrolled down). Only shows after visiting /?vvdebug=1 on
that device (stored in localStorage); /?vvdebug=0 turns it off. Remove in the next fix version.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v873.js'
dst = '_deploy/assets/index-DUcNPOLc-v874.js'

content = open(src, encoding='utf-8').read()

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
  'dvh '+Math.round(window.__vvp?window.__vvp.dvh:0)+' svh '+Math.round(window.__vvp?window.__vvp.svh:0)+' lvh '+Math.round(window.__vvp?window.__vvp.lvh:0)+'\n'+
  st.log.slice(-3).join('\n');
};
const p=document.createElement('div');p.style.cssText='position:absolute;visibility:hidden;pointer-events:none;width:1px;height:100dvh';document.body.appendChild(p);
const p2=p.cloneNode();p2.style.height='100svh';document.body.appendChild(p2);
const p3=p.cloneNode();p3.style.height='100lvh';document.body.appendChild(p3);
const meas=()=>{window.__vvp={dvh:p.offsetHeight,svh:p2.offsetHeight,lvh:p3.offsetHeight}};
document.addEventListener('touchstart',e=>{if(e.target.closest&&e.target.closest('.search-input')){st.tapY=Math.round(scrollY);st.maxOff=0;st.maxDY=0;st.log=[]}},{passive:true,capture:true});
document.addEventListener('focusin',e=>{if(e.target.classList&&e.target.classList.contains('search-input')){st.focusY=Math.round(scrollY);const t0=performance.now();
 [100,300,600,1000,1500].forEach(ms=>setTimeout(()=>{st.log.push(ms+'ms y'+Math.round(scrollY)+' off'+Math.round(vv?vv.offsetTop:0)+' vh'+Math.round(vv?vv.height:0)+' ih'+innerHeight+' shell'+r('.search-shell'));draw()},ms))}},true);
const tick=()=>{meas();draw()};
if(vv){vv.addEventListener('resize',tick);vv.addEventListener('scroll',tick)}
addEventListener('scroll',tick,{passive:true});
setInterval(tick,250);tick();
}catch(e){}})();
'''

if 'vvdebug' in content:
    print('FAIL: readout already present')
    sys.exit(1)
content = content + READOUT
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
