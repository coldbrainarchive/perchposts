#!/usr/bin/env python3
"""Patch v1142 -> v1143:
- A flap / post-worm notification tapped while you're already on that post still opens Reactions and flashes the row
  (the notification sends a "pp-rx" event instead of navigating to the same page).
- The row flash is the same as a chirp's notification flash (chat-flash: two pulses then a fade, in the person's colour)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1142.js'
dst = '_deploy/assets/index-DUcNPOLc-v1143.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# Reactions: one highlight function, used on arrival and on the pp-rx-hl event; chirp-style flash in the bird's colour
old_eff = (" (0,_.useEffect)(()=>{const h=window._ppRxHL;if(!h||h.id!==id||!ppl)return;window._ppRxHL=null;setTab(`all`);\n"
  "  setTimeout(()=>{const w=_hlR.current;if(!w)return;const el=[...w.querySelectorAll(`.rx-row[data-kd=\"${h.k}\"]`)].find(x=>x.dataset.gpb===h.u);if(!el)return;\n"
  "   el.scrollIntoView({behavior:`smooth`,block:`center`});el.classList.remove(`pr-hl`,`pr-hl-w`);void el.offsetWidth;el.classList.add(h.k===`w`?`pr-hl-w`:`pr-hl`);setTimeout(()=>el.classList.remove(`pr-hl`,`pr-hl-w`),3200)},500)},[id,ppl]);\n")
new_eff = (" const _doHL=()=>{const h=window._ppRxHL;if(!h||h.id!==id||!ppl)return;window._ppRxHL=null;setTab(`all`);\n"
  "  setTimeout(()=>{const w=_hlR.current;if(!w)return;const el=[...w.querySelectorAll(`.rx-row[data-kd=\"${h.k}\"]`)].find(x=>x.dataset.gpb===h.u);if(!el)return;\n"
  "   el.scrollIntoView({behavior:`smooth`,block:`center`});const nm=el.querySelector(`.rx-nm`),m=nm&&getComputedStyle(nm).color.match(/(\\d+),\\s*(\\d+),\\s*(\\d+)/);el.style.setProperty(`--gc`,m?`${m[1]},${m[2]},${m[3]}`:`192,132,252`);\n"
  "   clearTimeout(el._gt);el.classList.remove(`chat-flash`);void el.offsetWidth;el.classList.add(`chat-flash`);el._gt=setTimeout(()=>el.classList.remove(`chat-flash`),2600)},450)};\n"
  " (0,_.useEffect)(_doHL,[id,ppl]);(0,_.useEffect)(()=>{const f=()=>_doHL();addEventListener(`pp-rx-hl`,f);return()=>removeEventListener(`pp-rx-hl`,f)},[id,ppl]);\n")
patch(old_eff, new_eff, 'chirp-style flash, reusable')
# post page: pp-rx event (same post) opens Reactions, then asks the list to flash
patch("(0,_.useEffect)(()=>{let _f=()=>_setCF(!1);window.addEventListener(`popstate`,_f);return()=>window.removeEventListener(`popstate`,_f)},[]);",
      "(0,_.useEffect)(()=>{let _f=()=>_setCF(!1);window.addEventListener(`popstate`,_f);return()=>window.removeEventListener(`popstate`,_f)},[]);"
      "(0,_.useEffect)(()=>{const _f=ev=>{const d=ev.detail||{};if(d.id!==r)return;window._ppRxHL=d;if(_cf)_closeC();_setCpm(`react`);setTimeout(()=>{document.querySelector(`.comments-shell`)?.scrollIntoView({behavior:`smooth`,block:`start`});dispatchEvent(new CustomEvent(`pp-rx-hl`))},350)};addEventListener(`pp-rx`,_f);return()=>removeEventListener(`pp-rx`,_f)},[r,_cf]);",
      'post page listens for pp-rx')
# notification tap on the post you're already on
patch("onClick:_ev=>{if(e.req&&e.req.kind===`invite`&&e.req.status!==`accepted`){_ev.preventDefault();_nMark(e);return}_nTap(_ev);_nMark(e);a()}",
      "onClick:_ev=>{if(e.req&&e.req.kind===`invite`&&e.req.status!==`accepted`){_ev.preventDefault();_nMark(e);return}"
      "if((e.type===`vote`||e.type===`worm`&&!e.targetId)&&e.postId&&location.pathname===`/post/${e.postId}`){_ev.preventDefault();_nMark(e);a();const _d={id:e.postId,k:e.type===`vote`?`f`:`w`,u:String(e.text||``).split(` `)[0]};setTimeout(()=>dispatchEvent(new CustomEvent(`pp-rx`,{detail:_d})),80);return}"
      "_nTap(_ev);_nMark(e);a()}", 'same-post notification')
# old glow styles no longer used
for k in ["@keyframes prhl{0%,55%{box-shadow:0 0 0 2px #c084fc,0 0 18px rgba(192,132,252,.65)}100%{box-shadow:0 0 0 0 transparent}}",
          "@keyframes prhlw{0%,55%{box-shadow:0 0 0 2px #fb7185,0 0 18px rgba(251,113,133,.6)}100%{box-shadow:0 0 0 0 transparent}}",
          "body .rx-row.pr-hl{animation:prhl 3s ease-out}body .rx-row.pr-hl-w{animation:prhlw 3s ease-out}"]:
    patch(k, "", 'drop old glow')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
