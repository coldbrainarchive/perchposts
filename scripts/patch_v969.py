#!/usr/bin/env python3
"""Patch v968 -> v969: desktop post page keeps the message box on screen.
- Wider than 900px (where the chat is a panel under the post, not the phone full-screen chat), the chat
  panel's compose bar is pinned to the bottom of the window at the panel's width, 18px up, so it lines up
  with the panel's bottom once the panel is scrolled into place. Until then it floats as a rounded bar
  over the page with a shadow; when docked it merges into the panel (square top, panel border).
- The panel keeps room for it, so the newest chirps never hide behind it.
- Clicking into the box scrolls the page smoothly to the chat so you see the conversation while typing."""
src = '_deploy/assets/index-DUcNPOLc-v968.js'
dst = '_deploy/assets/index-DUcNPOLc-v969.js'
c = open(src, encoding='utf-8').read()
c += r'''
;(()=>{try{
 const H=document.documentElement,mq=matchMedia(`(min-width: 901px)`);
 const shell=()=>document.querySelector(`.comments-shell:not(.chat-full):not(.chat-preview)`);
 const sync=()=>{const sh=shell(),on=!!(sh&&mq.matches&&sh.querySelector(`.chat-compose`));H.classList.toggle(`dc-on`,on);if(!on)return;
  const r=sh.getBoundingClientRect(),cp=sh.querySelector(`.chat-compose`);
  H.style.setProperty(`--dcL`,(r.left+1)+`px`);H.style.setProperty(`--dcW`,(r.width-2)+`px`);H.style.setProperty(`--dcH`,cp.offsetHeight+`px`);
  H.classList.toggle(`dc-docked`,Math.abs(r.bottom-(innerHeight-18))<3)};
 let raf=0;const kick=()=>{cancelAnimationFrame(raf);raf=requestAnimationFrame(sync)};
 addEventListener(`resize`,kick);addEventListener(`scroll`,kick,{passive:!0});setInterval(sync,400);
 document.addEventListener(`focusin`,e=>{const t=e.target;if(!H.classList.contains(`dc-on`)||!t.closest||!t.closest(`.chat-compose`))return;
  const sh=shell();if(!sh)return;const d=sh.getBoundingClientRect().top-73;if(d>4)scrollTo({top:scrollY+d,behavior:matchMedia(`(prefers-reduced-motion: reduce)`).matches?`auto`:`smooth`})});
 const s=document.createElement(`style`);s.textContent=`
html.dc-on .comments-shell:not(.chat-full):not(.chat-preview){padding-bottom:var(--dcH,70px);box-sizing:border-box}
html.dc-on .comments-shell:not(.chat-full):not(.chat-preview) .chat-compose{position:fixed;left:var(--dcL);width:var(--dcW);bottom:19px;z-index:30;box-sizing:border-box;border-radius:16px;border:1px solid #2e303a;box-shadow:0 -10px 30px rgba(0,0,0,.45);transition:border-radius .15s,box-shadow .15s}
html.dc-on.dc-docked .comments-shell:not(.chat-full):not(.chat-preview) .chat-compose{border-radius:0 0 17px 17px;border:0;border-top:1px solid rgba(148,163,184,.1);box-shadow:none}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
