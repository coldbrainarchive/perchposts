#!/usr/bin/env python3
"""Patch v1352 -> v1353: the story dots sit exactly on the logo globe's grid crossings (a vertical line meets one
of the 3 horizontal lines), computed from the same geometry the logo draws (meridian arcs every 30 deg turned by
the spin angle, parallels at y=30/50/70 with the same curve), so they move exactly with the lines. Up to 6 dots:
6 fixed crossings, 3 on the front and their 3 mirror crossings on the back. With 1-3 new stories each gets a dot on
both sides (one always faces you whichever way the spin stops); with 4-6 each gets one."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1352.js'
dst = '_deploy/assets/index-DUcNPOLc-v1353.js'
c = open(src, encoding='utf-8').read()
a = c.index("  const R=L.getBoundingClientRect().width*.727/2*.78,lat0=22*Math.PI/180,D=Math.PI/180;")
b = c.index("  if(!sh.length){st.textContent=`.pp-logo::after{content:none}`;return}", a)
c = c[:a] + r"""  // logo geometry (viewBox 0 -10 100 110): globe centre (56,50) r 38; vertical lines at 15+30k deg turned by the spin
  const br=L.getBoundingClientRect(),W=br.width,H=br.height,sc=Math.min(W/100,H/110),ox=(W-100*sc)/2,oy=(H-110*sc)/2,D=Math.PI/180;
  const phi=(window._ppSpin&&window._ppSpin.phi)||0;
  const SLOTS=[[10,`u`],[1,`e`],[0,`d`],[4,`u`],[7,`e`],[6,`d`]];   // slot i+3 is directly behind slot i
  const list=fresh.slice(0,6),use=[];
  if(list.length<=3)list.forEach((s,i)=>{use.push([s,SLOTS[i]],[s,SLOTS[i+3]])});else list.forEach((s,i)=>use.push([s,SLOTS[i]]));
  const par=(j,x)=>{const t=Math.min(1,Math.max(0,(x-16)/80));return j===`e`?50:j===`u`?30+14*t*(1-t):70-14*t*(1-t)};
  const sh=[];for(const[i,[k,j]]of use){const p=(15+30*k+phi)*D,cs=Math.cos(p);if(cs<.06)continue;
   let x=56,y=par(j,56);for(let n=0;n<4;n++){const dy=(y-50)/38;x=56+38*Math.sin(p)*Math.sqrt(Math.max(0,1-dy*dy));y=par(j,x)}
   const X=(ox+x*sc).toFixed(1),Y=(oy+(y+10)*sc).toFixed(1),z=Math.min(1,cs*2.6),col=COLORS[i%COLORS.length];
   sh.push(`${X}px ${Y}px 0 ${(2.3*z).toFixed(2)}px ${col}`,`${X}px ${Y}px ${(6*z).toFixed(1)}px ${(2.6*z).toFixed(1)}px ${col}99`)}
""" + c[b:]
old = "st.textContent=`.pp-logo::after{content:\"\";position:absolute;left:55.5%;top:52.7%;width:0;height:0;"
if c.count(old) != 1: print('FAIL anchor', c.count(old)); sys.exit(1)
c = c.replace(old, "st.textContent=`.pp-logo::after{content:\"\";position:absolute;left:0;top:0;width:0;height:0;")
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
