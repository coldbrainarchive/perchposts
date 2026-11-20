#!/usr/bin/env python3
"""Patch v1256 -> v1257: the header globe spins slowly, like the earth, while the title shows the countdown clock.
The speed is planned so the globe lands exactly on its normal position as "perchposts" finishes flipping back
(or at 00:00 when the hour's batch drops), so the bird's moves always start from rest.
- The globe's grid is the same after half a turn, so the spin is whole half-turns (~15 s each, gentle ease in/out).
- Grid lines move left to right (earth's direction as seen from the front).
- Never draws over a bird move; skipped with prefers-reduced-motion; drawn at ~30 fps to go easy on phones."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1256.js'
dst = '_deploy/assets/index-DUcNPOLc-v1257.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# clock starts: plan the spin to end when the title will be back to "perchposts" (or at the hour)
patch("await show(mmss(),!0,!0);mode=`time`;busy=!1;nextAt=Date.now()+EVERY}",
      "await show(mmss(),!0,!0);mode=`time`;busy=!1;nextAt=Date.now()+EVERY;try{const _l=left();window._ppSpin&&window._ppSpin.start(_l-EVERY/1000>15?Math.ceil(nextAt/1000)*1000+5+1250:Date.now()+_l*1000)}catch(e){}}",
      'spin while the clock shows')
# back to the brand: make sure it lands as the letters finish
patch("async function toBrand(){await show(`perchposts`,!0,!1);",
      "async function toBrand(){try{window._ppSpin&&window._ppSpin.settle(1250)}catch(e){}await show(`perchposts`,!0,!1);", 'land on brand')
patch("busy=!0;await show(`00:00     `,!1);", "busy=!0;try{window._ppSpin&&window._ppSpin.settle(250)}catch(e){}await show(`00:00     `,!1);", 'land at 00:00')
JS = r"""
;window._ppSpin=(()=>{try{
const B=window.ppBird;if(!B)return null;
const HALF=15000,RAMP=1800,FRAME=33;
const still=()=>window.matchMedia&&window.matchMedia(`(prefers-reduced-motion: reduce)`).matches;
const logos=()=>[...document.querySelectorAll(`.pp-logo`)];
let plan=null,raf=0,lastDraw=0;
// share of the distance covered at time u (0..D): speeds up over r, steady, slows down over r
const prof=(u,D,r)=>{r=Math.min(r,D/2);const v=1/(D-r);if(u<=0)return 0;if(u>=D)return 1;if(u<r)return v*u*u/(2*r);if(u<D-r)return v*(r/2+(u-r));const w=D-u;return 1-v*w*w/(2*r)};
const eOut=x=>1-Math.pow(1-x,3);
const phiAt=t=>{if(!plan)return 0;const u=t-plan.t0,D=plan.t1-plan.t0;return plan.p0+(plan.p1-plan.p0)*(plan.out?eOut(Math.min(1,Math.max(0,u/D))):prof(u,D,plan.r))};
const draw=(pose)=>logos().forEach((el,i)=>{if(!el._ppBusy)el.innerHTML=B.svg(pose,`s`+i)});
function frame(t){raf=0;if(!plan)return;
  if(t>=plan.t1){plan=null;draw(B.REST);return}
  if(t-lastDraw>=FRAME){lastDraw=t;draw({...B.REST,th:phiAt(t)%180})}
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
}catch(e){console.error(e);return null}})();
"""
c = c + JS
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
