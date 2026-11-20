#!/usr/bin/env python3
"""Patch v1259 -> v1260:
1. The mod/admin badge globe (next to names) gets the evenly spaced lines too: meridians at ±15/±45
   (rx 11.39 / 31.11 on its r=44 circle) instead of rx 16 / 32.
2. Smoother spin. Rebuilding the whole glowing logo every frame made the browser redo two blur filters per
   frame, which stuttered. Now the logo (with its glow, minus the moving lines) is drawn once when the spin
   starts, and only a light overlay of 12 line paths is updated each frame (no filters, no HTML rebuild).
   At the end the normal resting logo is drawn back in, exactly as before."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1259.js'
dst = '_deploy/assets/index-DUcNPOLc-v1260.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("rx:`16`,ry:`44`", "rx:`11.39`,ry:`44`", 'badge inner meridians', n=2)
patch("rx:`32`,ry:`44`", "rx:`31.11`,ry:`44`", 'badge outer meridians', n=2)
patch("${meridians(pose.th)}</g>", "${pose.noMer ? \"\" : meridians(pose.th)}</g>", 'logo without lines (spin base)')
i = c.find(";window._ppSpin=(()=>{try{"); j = c.find("}catch(e){console.error(e);return null}})();", i) + len("}catch(e){console.error(e);return null}})();")
assert i > 0 and j > i
c = c[:i] + r""";window._ppSpin=(()=>{try{
const B=window.ppBird;if(!B)return null;
const HALF=15000,RAMP=1800,CX=56,R=38,DG=Math.PI/180,MER=Array.from({length:12},(_,k)=>15+30*k);
const still=()=>window.matchMedia&&window.matchMedia(`(prefers-reduced-motion: reduce)`).matches;
const logos=()=>[...document.querySelectorAll(`.pp-logo`)];
let plan=null,raf=0;
// share of the distance covered at time u (0..D): speeds up over r, steady, slows down over r
const prof=(u,D,r)=>{r=Math.min(r,D/2);const v=1/(D-r);if(u<=0)return 0;if(u>=D)return 1;if(u<r)return v*u*u/(2*r);if(u<D-r)return v*(r/2+(u-r));const w=D-u;return 1-v*w*w/(2*r)};
const eOut=x=>1-Math.pow(1-x,3);
const phiAt=t=>{if(!plan)return 0;const u=t-plan.t0,D=plan.t1-plan.t0;return plan.p0+(plan.p1-plan.p0)*(plan.out?eOut(Math.min(1,Math.max(0,u/D))):prof(u,D,plan.r))};
// spin layer: the logo drawn once without its up-and-down lines, plus a light overlay holding just those lines
const P12=w=>MER.map(()=>`<path${w}/>`).join(``);
function setup(el,i){el.innerHTML=B.svg({...B.REST,noMer:1},`s`+i)+
  `<svg class="pp-spin-ov" viewBox="0 -10 100 110" style="position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible;pointer-events:none" aria-hidden="true">`+
  `<defs><clipPath id="spc${i}"><circle cx="56" cy="50" r="35.7"/></clipPath></defs><g fill="none" stroke="#c084fc" stroke-linecap="round" clip-path="url(#spc${i})">`+
  `<g opacity=".12" stroke-width="4">${P12(``)}</g><g stroke-width="1.6">${P12(``)}</g></g></svg>`;
  const ps=[...el.querySelectorAll(`.pp-spin-ov path`)];el._spinP=[ps.slice(0,12),ps.slice(12)];el._spinOn=1}
function lines(el,th){const [g,l]=el._spinP;for(let k=0;k<12;k++){const p=(MER[k]+th)*DG;let d=``;
  if(Math.cos(p)>0.001){const rx=Math.abs(R*Math.sin(p));d=rx<0.4?`M ${CX} 12 L ${CX} 88`:`M ${CX} 12 A ${rx.toFixed(2)} ${R} 0 0 ${Math.sin(p)>0?1:0} ${CX} 88`}
  if(g[k]._d!==d){g[k]._d=d;g[k].setAttribute(`d`,d);l[k].setAttribute(`d`,d)}}}
function rest(){logos().forEach((el,i)=>{if(el._spinOn){el._spinOn=0;el._spinP=null;if(!el._ppBusy)el.innerHTML=B.svg(B.REST,`s`+i)}})}
function frame(t){raf=0;if(!plan)return;
  if(t>=plan.t1){plan=null;rest();return}
  const th=phiAt(t)%180;
  logos().forEach((el,i)=>{if(el._ppBusy)return;if(!el._spinOn||!el.contains(el._spinP&&el._spinP[1][0]))setup(el,i);lines(el,th)});
  raf=requestAnimationFrame(frame)}
const go=()=>{if(!raf)raf=requestAnimationFrame(frame)};
return{
  start(endWall){if(still())return;const now=performance.now(),D=endWall-Date.now();if(D<4000)return;
    const p0=plan?phiAt(now):0,n=Math.max(1,Math.round(D/HALF));
    plan={t0:now,t1:now+D,p0,p1:Math.ceil(p0/180)*180+180*n,r:RAMP};go()},
  // land on the rest position in ms (only if the plan isn't already landing then)
  settle(ms){if(!plan)return;const now=performance.now();if(Math.abs(plan.t1-(now+ms))<500)return;
    const p=phiAt(now);const to=Math.ceil(p/180)*180;plan={t0:now,t1:now+Math.max(ms,200),p0:p,p1:to,out:1};go()},
  get on(){return!!plan}};
}catch(e){console.error(e);return null}})();""" + c[j:]
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
b = open('brand/pp-bird.js', encoding='utf-8').read()
assert b.count("${meridians(pose.th)}</g>") == 1
open('brand/pp-bird.js', 'w', encoding='utf-8').write(b.replace("${meridians(pose.th)}</g>", "${pose.noMer ? \"\" : meridians(pose.th)}</g>")); print('brand/pp-bird.js updated')
