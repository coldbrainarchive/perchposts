#!/usr/bin/env python3
"""Patch v1348 -> v1349: "new stories" dot on the globe logo. Every 5 minutes (and when you come back to the tab)
the page reads /globe-sig; if a story in the top 12 has none of its first posts among what this device saw on the
globe (localStorage pp_globe_seen, written by the globe page), the logo gets a red dot and a purple radar pulse
(keeps pulsing until you open the globe; no pulse with Reduce Motion)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1348.js'
dst = '_deploy/assets/index-DUcNPOLc-v1349.js'
c = open(src, encoding='utf-8').read()
c += r"""
;(()=>{try{
 const st=document.createElement(`style`);st.textContent=`html.gl-new .pp-logo::after{content:"";position:absolute;top:1px;right:0;width:11px;height:11px;border-radius:999px;background:#ef4444;box-shadow:0 0 0 2px #0b0c10;z-index:3;pointer-events:none}
html.gl-new .pp-logo::before{content:"";position:absolute;inset:3px;border-radius:999px;border:2px solid #c084fc;box-shadow:0 0 10px rgba(192,132,252,.55);animation:glPulse 2.4s ease-out infinite;pointer-events:none;z-index:0}
@keyframes glPulse{0%{transform:scale(.9);opacity:.9}100%{transform:scale(1.9);opacity:0}}
@media (prefers-reduced-motion: reduce){html.gl-new .pp-logo::before{animation:none;opacity:0}}`;document.head.appendChild(st);
 const seen=()=>{try{return new Set(JSON.parse(localStorage.getItem(`pp_globe_seen`)||`[]`))}catch(e){return new Set()}};
 const check=()=>{if(document.hidden)return;fetch(`${R}/globe-sig`).then(r=>r.ok?r.json():null).then(d=>{if(!d||!Array.isArray(d.s))return;const s=seen();
   const fresh=d.s.some(ids=>Array.isArray(ids)&&ids.length&&!ids.some(id=>s.has(id)));document.documentElement.classList.toggle(`gl-new`,fresh)}).catch(()=>{})};
 setTimeout(check,1500);setInterval(check,5*60e3);document.addEventListener(`visibilitychange`,()=>{if(!document.hidden)check()});
}catch(e){}})();
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
