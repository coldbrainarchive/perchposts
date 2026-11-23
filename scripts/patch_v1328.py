#!/usr/bin/env python3
"""Patch v1327 -> v1328: on feed cards of posts with a flock tag, the flock tag stays open and the perch tag and
region/country collapse to their icon in a wider oval (36px, like a collapsed name pill). Tapping a collapsed pill
opens them all (like a collapsed name pill); tapping elsewhere closes. Posts without a flock tag are unchanged.
The scroller's top row and the post page still show every tag in full."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1327.js'
dst = '_deploy/assets/index-DUcNPOLc-v1328.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("d&&!e.board_auto&&(0,L.jsx)(`button`,{type:`button`,onClick:e=>g?m(`board`,g,e):e.stopPropagation(),style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(Ar,{boardName:d,small:!0})}),(e.country||e.continent)&&(0,L.jsx)(`span`,{style:{cursor:`pointer`,display:`inline-flex`,alignItems:`center`},",
      "d&&!e.board_auto&&(0,L.jsx)(`button`,{type:`button`,className:e.utag?`tg-c`:void 0,onClick:e=>g?m(`board`,g,e):e.stopPropagation(),style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(Ar,{boardName:d,small:!0})}),(e.country||e.continent)&&(0,L.jsx)(`span`,{className:e.utag?`tg-c`:void 0,style:{cursor:`pointer`,display:`inline-flex`,alignItems:`center`},", 'mark collapsible pills')
patch("body .lb-ic{", "body .feed-post-card:not(.tg-open) .tg-c .pp-tag{width:36px;padding:0!important;justify-content:center;gap:0!important}body .feed-post-card:not(.tg-open) .tg-c .pp-tag>span:last-child{display:none}body .feed-post-card.tg-open .tg-c .pp-tag>span:last-child{animation:cuFade .3s ease-out}body .lb-ic{", 'css')
c += r"""
;(()=>{try{document.addEventListener(`click`,e=>{const t=e.target,tc=t&&t.closest&&t.closest(`.tg-c`);const card=tc&&tc.closest(`.feed-post-card`);
  if(card&&!card.classList.contains(`tg-open`)){e.preventDefault();e.stopPropagation();document.querySelectorAll(`.feed-post-card.tg-open`).forEach(x=>x.classList.remove(`tg-open`));card.classList.add(`tg-open`);return}
  document.querySelectorAll(`.feed-post-card.tg-open`).forEach(x=>{if(!x.contains(t))x.classList.remove(`tg-open`)})},!0)}catch(e){}})();
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
