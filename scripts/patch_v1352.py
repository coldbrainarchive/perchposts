#!/usr/bin/env python3
"""Patch v1351 -> v1352: the story dots on the globe logo turn with the logo's spin (same angle as its meridian
lines), so dots on the back slide out of view and others come round. All new stories get a dot (not just 3);
only the ones on the facing side show. At rest the view faces the newest story so at least one dot is visible."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1351.js'
dst = '_deploy/assets/index-DUcNPOLc-v1352.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
# expose the spin angle (and remember where it stopped)
patch("let plan=null,raf=0;\n// share of the distance", "let plan=null,raf=0,restPhi=0;\n// share of the distance", 'restPhi var')
patch("  if(t>=plan.t1){plan=null;rest();return}", "  if(t>=plan.t1){restPhi=plan.p1%360;plan=null;rest();return}", 'remember rest')
patch("const p0=plan?phiAt(now):0,n=Math.max(1,Math.round(D/HALF));", "const p0=plan?phiAt(now):restPhi,n=Math.max(1,Math.round(D/HALF));", 'start from rest')
patch("  get on(){return!!plan}};", "  get on(){return!!plan},\n  // degrees the globe has turned (the meridian lines' angle; the dots use it too)\n  get phi(){return plan?phiAt(performance.now()):restPhi}};", 'phi getter')

# dots: redraw from the spin angle every frame while spinning
a = c.index("  const R=L.getBoundingClientRect().width*.727/2*.78,lat0=22*Math.PI/180,lng0=14*Math.PI/180,used=[];")
b = c.index("st.textContent=`.pp-logo::after{content:", a)
c = c[:a] + r"""  const R=L.getBoundingClientRect().width*.727/2*.78,lat0=22*Math.PI/180,D=Math.PI/180;
  // rest view faces the newest story; the logo's spin turns everything by the same angle as its lines
  const lead=fresh.find(i=>last.o&&last.o[i]),lng0=(lead!=null?last.o[lead][1]:14)*D,spin=(window._ppSpin&&window._ppSpin.phi||0)*D;
  const sh=[];fresh.forEach((i,k)=>{const o=last.o&&last.o[i];let la,lo;
   if(o){la=o[0]*D;lo=o[1]*D-lng0+spin}else{la=(10+k*7)*D;lo=(k*47)*D+spin}
   const front=Math.sin(lat0)*Math.sin(la)+Math.cos(lat0)*Math.cos(la)*Math.cos(lo);if(front<.08)return;
   const x=Math.cos(la)*Math.sin(lo),y=Math.cos(lat0)*Math.sin(la)-Math.sin(lat0)*Math.cos(la)*Math.cos(lo);
   const dx=(x*R).toFixed(1),dy=(-y*R).toFixed(1),z=Math.min(1,front*2.2),col=COLORS[i%COLORS.length];
   sh.push(`${dx}px ${dy}px 0 ${(2.4*z).toFixed(2)}px ${col}`,`${dx}px ${dy}px ${(7*z).toFixed(1)}px ${(3*z).toFixed(1)}px ${col}99`)});
  if(!sh.length){st.textContent=`.pp-logo::after{content:none}`;return}
  """ + c[b:]
patch("box-shadow:${sh.join(`,`)};animation:glTw 2.8s ease-in-out infinite}", "box-shadow:${sh.join(`,`)};animation:glTw 2.8s ease-in-out infinite}", 'shadow join kept')
patch(" setTimeout(check,1500);setInterval(check,5*60e3);document.addEventListener(`visibilitychange`,()=>{if(!document.hidden)check()});addEventListener(`resize`,draw);",
      " setTimeout(check,1500);setInterval(check,5*60e3);document.addEventListener(`visibilitychange`,()=>{if(!document.hidden)check()});addEventListener(`resize`,draw);\n // follow the spin frame by frame while the logo is turning\n let spinning=!1;const tick=()=>{const on=!!(window._ppSpin&&window._ppSpin.on);if(on||spinning)draw();spinning=on;requestAnimationFrame(tick)};requestAnimationFrame(tick);", 'spin follow')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
