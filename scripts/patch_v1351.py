#!/usr/bin/env python3
"""Patch v1350 -> v1351: replace the red dot + purple radar pulse on the globe logo (user's pick, option 1) with up
to 3 tiny glowing story dots on the logo's globe, in the new stories' colours (same order as the globe page),
each placed where its story happened on a small view of the Earth. They show only while a story you haven't seen
on the globe is in the top 12, and go once you open the globe. Drawn with one ::after + box-shadows so the logo's
own animation (which rewrites its svg) can't remove them."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1350.js'
dst = '_deploy/assets/index-DUcNPOLc-v1351.js'
c = open(src, encoding='utf-8').read()
a = c.index(';(()=>{try{\n const st=document.createElement(`style`);st.textContent=`html.gl-new .pp-logo::after')
b = c.index('}catch(e){}})();', a) + len('}catch(e){}})();')
c = c[:a] + r""";(()=>{try{
 // New stories on the globe: tiny glowing dots on the logo's globe (story colours, where the story happened)
 const COLORS=[`#c084fc`,`#2dd4bf`,`#fbbf24`,`#f87171`,`#60a5fa`,`#4ade80`,`#fb923c`,`#f472b6`,`#a3e635`,`#38bdf8`,`#e879f9`,`#facc15`];
 const st=document.createElement(`style`);document.head.appendChild(st);
 let last=null;
 const seen=()=>{try{return new Set(JSON.parse(localStorage.getItem(`pp_globe_seen`)||`[]`))}catch(e){return new Set()}};
 const draw=()=>{const L=document.querySelector(`.pp-logo`);if(!last||!L){st.textContent=``;return}
  const s=seen(),fresh=[];last.s.forEach((ids,i)=>{if(Array.isArray(ids)&&ids.length&&!ids.some(id=>s.has(id)))fresh.push(i)});
  if(!fresh.length){st.textContent=``;return}
  const R=L.getBoundingClientRect().width*.727/2*.78,lat0=22*Math.PI/180,lng0=14*Math.PI/180,used=[];
  const sh=fresh.slice(0,3).map((i,k)=>{const o=last.o&&last.o[i];let x=0,y=0;
   if(o){const la=o[0]*Math.PI/180,lo=o[1]*Math.PI/180-lng0;x=Math.cos(la)*Math.sin(lo);y=Math.cos(lat0)*Math.sin(la)-Math.sin(lat0)*Math.cos(la)*Math.cos(lo);
    const front=Math.sin(lat0)*Math.sin(la)+Math.cos(lat0)*Math.cos(la)*Math.cos(lo);if(front<0){const n=Math.hypot(x,y)||1;x=x/n*.9;y=y/n*.9}}
   else{const a=k*2.1+.6;x=Math.cos(a)*.55;y=Math.sin(a)*.55}
   let dx=x*R,dy=-y*R;for(const u of used){if(Math.hypot(dx-u[0],dy-u[1])<5){dx+=4;dy-=3}}used.push([dx,dy]);
   const col=COLORS[i%COLORS.length];return`${dx.toFixed(1)}px ${dy.toFixed(1)}px 0 2.4px ${col}, ${dx.toFixed(1)}px ${dy.toFixed(1)}px 7px 3px ${col}99`});
  st.textContent=`.pp-logo::after{content:"";position:absolute;left:55.5%;top:52.7%;width:0;height:0;border-radius:999px;z-index:3;pointer-events:none;box-shadow:${sh.join(`,`)};animation:glTw 2.8s ease-in-out infinite}
@keyframes glTw{0%,100%{opacity:1}50%{opacity:.55}}
@media (prefers-reduced-motion: reduce){.pp-logo::after{animation:none}}`};
 const check=()=>{if(document.hidden)return;fetch(`${R}/globe-sig`).then(r=>r.ok?r.json():null).then(d=>{if(!d||!Array.isArray(d.s))return;last=d;draw()}).catch(()=>{})};
 setTimeout(check,1500);setInterval(check,5*60e3);document.addEventListener(`visibilitychange`,()=>{if(!document.hidden)check()});addEventListener(`resize`,draw);
}catch(e){}})();""" + c[b:]
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
