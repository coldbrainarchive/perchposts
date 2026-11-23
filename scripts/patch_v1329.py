#!/usr/bin/env python3
"""Patch v1328 -> v1329: collapsed tags everywhere for birds' posts with a flock tag + scroller tag-tap fix.
- Bug: the scroller filters by clicking the feed card's matching pill; that click (synthetic) was caught by the
  collapse logic and only opened the card's tags. Synthetic clicks now skip it, so they filter again.
- Post page: perch tag and region/country collapse to icon ovals when the post has a flock tag (tap opens all).
- Scroller top row: same — flock tag open, the others as icon ovals; tapping a collapsed one opens the row, tapping an
  open one filters as before."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1328.js'
dst = '_deploy/assets/index-DUcNPOLc-v1329.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# 1) synthetic clicks skip the collapse logic
patch(";(()=>{try{document.addEventListener(`click`,e=>{const t=e.target,tc=t&&t.closest&&t.closest(`.tg-c`);",
      ";(()=>{try{document.addEventListener(`click`,e=>{if(!e.isTrusted)return;const t=e.target,tc=t&&t.closest&&t.closest(`.tg-c`);", 'skip synthetic clicks')
# 2) post page
patch("ce&&!c.board_auto&&(()=>{let e=nr.find(e=>e.name===ce)?.slug;return e?(0,L.jsx)(I,{to:`/?board=${e}`,style:{textDecoration:`none`,display:`inline-flex`,alignItems:`center`},children:(0,L.jsx)(Ar,{boardName:ce,small:!0})}):(0,L.jsx)(Ar,{boardName:ce,small:!0})})(),(c.country||c.continent)&&(0,L.jsxs)(`button`,{type:`button`,onClick:",
      "ce&&!c.board_auto&&(()=>{let e=nr.find(e=>e.name===ce)?.slug;return e?(0,L.jsx)(I,{to:`/?board=${e}`,className:c.utag?`tg-c`:void 0,style:{textDecoration:`none`,display:`inline-flex`,alignItems:`center`},children:(0,L.jsx)(Ar,{boardName:ce,small:!0})}):(0,L.jsx)(`span`,{className:c.utag?`tg-c`:void 0,style:{display:`inline-flex`},children:(0,L.jsx)(Ar,{boardName:ce,small:!0})})})(),(c.country||c.continent)&&(0,L.jsxs)(`button`,{type:`button`,className:c.utag?`tg-c`:void 0,onClick:", 'post page pills')
# 3) scroller: know which pill is the flock tag
patch("if(out.some(o=>o.t===t))continue;const sv=x.querySelector(`svg`);out.push({t,c:bg,el:x,ic:sv?sv.outerHTML:``})}",
      "if(out.some(o=>o.t===t))continue;const sv=x.querySelector(`svg`);out.push({t,c:bg,el:x,ic:sv?sv.outerHTML:``,fl:x.classList.contains(`utag-l`)})}", 'reel: flag flock tag')
patch("const tagRow=()=>{const tr=document.createElement(`div`);tr.className=`reel-tags`;for(const g of d.tags||[]){const sp=document.createElement(`span`);sp.className=`reel-tag`;sp.textContent=g.t;",
      "const tagRow=()=>{const tr=document.createElement(`div`);tr.className=`reel-tags`;const _hasFl=(d.tags||[]).some(x=>x.fl);for(const g of d.tags||[]){const sp=document.createElement(`span`);sp.className=`reel-tag`+(_hasFl&&!g.fl?` tc`:``);{const mm=String(g.t).match(/^([^\\p{L}\\p{N}\\s]+)\\s+(.+)$/u);if(mm){const fg=document.createElement(`span`);fg.className=`rt-f`;fg.textContent=mm[1];const tx=document.createElement(`span`);tx.className=`rt-t`;tx.textContent=` `+mm[2];sp.append(fg,tx)}else{const tx=document.createElement(`span`);tx.className=`rt-t`;tx.textContent=g.t;sp.append(tx)}}", 'reel: split label, mark collapsible')
patch("ov.addEventListener(`click`,e=>{const t=e.target.closest&&e.target.closest(`.reel-tag[data-ti]`);if(!t)return;",
      "ov.addEventListener(`click`,e=>{const t=e.target.closest&&e.target.closest(`.reel-tag[data-ti]`);if(!t){if(!(e.target.closest&&e.target.closest(`.reel-head`)))ov.querySelectorAll(`.reel-head.tg-open`).forEach(h=>h.classList.remove(`tg-open`));return}const hd=t.closest(`.reel-head`);if(t.classList.contains(`tc`)&&hd&&!hd.classList.contains(`tg-open`)){e.preventDefault();e.stopPropagation();hd.classList.add(`tg-open`);return}", 'reel: tap opens collapsed')
patch("body .lb-ic{", "body .reel-head:not(.tg-open) .reel-tag.tc .rt-t{display:none}body .reel-head:not(.tg-open) .reel-tag.tc{min-width:40px;justify-content:center;padding-left:0!important;padding-right:0!important}body .reel-head:not(.tg-open) .reel-tag.tc .reel-tic{margin-right:0}body .reel-head.tg-open .reel-tag.tc .rt-t{animation:cuFade .3s ease-out}body .reel-tag{display:inline-flex;align-items:center}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
