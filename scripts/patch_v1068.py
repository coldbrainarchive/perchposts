#!/usr/bin/env python3
"""Patch v1067 -> v1068: the header logo comes alive. Every 30 seconds it plays one move, in turn:
wink (head tilt + closed eye), look around (pupil glance), turn right (3D head turn and back).
- The bird is drawn from a pose by brand/pp-bird.js (included below), so the turn is a real 3D rotation.
- First move ~4s after the page loads. Nothing plays while the tab is hidden, or for people with Reduce Motion on.
- At rest the drawing matches the static logo, so nothing jumps."""
src = '_deploy/assets/index-DUcNPOLc-v1067.js'
dst = '_deploy/assets/index-DUcNPOLc-v1068.js'
c = open(src, encoding='utf-8').read()
bird = open('brand/pp-bird.js', encoding='utf-8').read()
c += '\n;' + bird + r'''
;(()=>{try{
 const B=window.ppBird;if(!B)return;
 const still=()=>window.matchMedia&&window.matchMedia(`(prefers-reduced-motion: reduce)`).matches;
 const logos=()=>[...document.querySelectorAll(`.pp-logo`)];
 // draw the logo with the pose renderer as soon as it appears, so animations start from an identical picture
 const init=()=>{for(const el of logos())if(!el._ppInit){el._ppInit=1;el._ppId=0;el.innerHTML=B.svg(B.REST)}};
 new MutationObserver(init).observe(document.documentElement,{childList:!0,subtree:!0});init();
 let n=0;const tick=()=>{if(document.visibilityState!==`visible`||still())return;init();const m=B.MOVES[n++%B.MOVES.length];for(const el of logos())B.play(el,m)};
 setTimeout(tick,4000);setInterval(tick,30000);
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
