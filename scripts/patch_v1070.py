#!/usr/bin/env python3
"""Patch v1067 -> v1070 (replaces v1068/v1069, which only appended the first animation):
animated header logo, with the turn now ending in a peck at the "p" of the name.
- brand/pp-bird.js draws the bird from a pose. Moves cycle every 30s: wink, look around, turn right.
  First move 15s after load; nothing plays while the tab is hidden or with Reduce Motion on.
- Turn right: faces right, inspects the "p" (~2s: leans back, cocks its head, eyes the letter), pecks it twice, turns back.
  How far it reaches is measured from the real gap to the "p", so it lands on phone and desktop.
- The "p" of "perchposts" is its own span (.pp-p) and wobbles each time the beak lands (ppbird-peck event)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1067.js'
dst = '_deploy/assets/index-DUcNPOLc-v1070.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('`perchposts`]}),(0,L.jsxs)(`div`,{className:`app-actions`',
      '(0,L.jsxs)(`span`,{className:`pp-name`,children:[(0,L.jsx)(`span`,{className:`pp-p`,children:`p`}),`erchposts`]})]}),(0,L.jsxs)(`div`,{className:`app-actions`', 'p of the name in its own span (name kept as one flex item)')
bird = open('brand/pp-bird.js', encoding='utf-8').read()
c += '\n;' + bird + r'''
;(()=>{try{
 const s=document.createElement(`style`);s.textContent=`
.app-brand .pp-p{display:inline-block;transform-origin:50% 85%}
.app-brand .pp-p.wig{animation:ppWig .55s cubic-bezier(.3,.7,.4,1)}
@keyframes ppWig{0%{transform:translateX(0) rotate(0)}18%{transform:translateX(2px) rotate(14deg)}40%{transform:translateX(1px) rotate(-9deg)}62%{transform:rotate(5deg)}82%{transform:rotate(-2deg)}100%{transform:rotate(0)}}
@media (prefers-reduced-motion:reduce){.app-brand .pp-p.wig{animation:none}}`;document.head.appendChild(s);
 const B=window.ppBird;if(!B)return;
 const still=()=>window.matchMedia&&window.matchMedia(`(prefers-reduced-motion: reduce)`).matches;
 const logos=()=>[...document.querySelectorAll(`.pp-logo`)];
 const init=()=>{for(const el of logos())if(!el._ppInit){el._ppInit=1;el._ppId=0;el.innerHTML=B.svg(B.REST)}};
 new MutationObserver(init).observe(document.documentElement,{childList:!0,subtree:!0});init();
 document.addEventListener(`ppbird-peck`,e=>{const b=e.target.closest&&e.target.closest(`.app-brand`);const p=b&&b.querySelector(`.pp-p`);if(!p)return;p.classList.remove(`wig`);void p.offsetWidth;p.classList.add(`wig`)});
 let n=0;const tick=()=>{if(document.visibilityState!==`visible`||still())return;init();const m=B.MOVES[n++%B.MOVES.length];
  for(const el of logos()){const b=el.closest(`.app-brand`),p=b&&b.querySelector(`.pp-p`);el._ppReach=p?B.reachTo(el,p):0;B.play(el,m)}};
 setTimeout(()=>{tick();setInterval(tick,30000)},15000);
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
