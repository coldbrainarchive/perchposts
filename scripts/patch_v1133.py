#!/usr/bin/env python3
"""Patch v1132 -> v1133:
- A chirp's reaction row: tapping "+N" expands it (wraps onto more lines, every emoji tappable) and opens the chirp's
  dropdown; the pill becomes "−" to collapse. Closing the chirp collapses it again.
- Who-reacted lists scroll instead of growing: about 5 rows show, the rest scroll inside a box with a fade at the
  bottom (gone at the end). Applies to the list under a chirp and to the post Reactions lists. "+N more" is gone."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1132.js'
dst = '_deploy/assets/index-DUcNPOLc-v1133.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# --- expandable reaction row ---
patch(" if(tot<=W+.5)return;\n m.style.display=`inline-flex`;m.setAttribute(`data-more`,`+`+ps.length);",
      " if(tot<=W+.5){row.classList.remove(`rx-open`);return}\n if(row.classList.contains(`rx-open`)){m.style.display=`inline-flex`;m.setAttribute(`data-more`,`−`);m.setAttribute(`aria-label`,`Show fewer reactions`);return}\n m.setAttribute(`aria-label`,`Show all reactions`);m.style.display=`inline-flex`;m.setAttribute(`data-more`,`+`+ps.length);",
      'row fit knows the open state')
patch("onClick:ev=>{ev.stopPropagation();_setRxW(null);y(!0)}},`__more`)",
      "onClick:ev=>{ev.stopPropagation();const r=ev.currentTarget.closest(`.rx-fit`),o=!r.classList.contains(`rx-open`);r.classList.toggle(`rx-open`,o);_rxFit(r);if(o){_setRxW(null);y(!0)}}},`__more`)",
      '+N expands / − collapses')
patch("onClick:()=>{if(p)return;_setRxW(null);y(e=>!e)},",
      "onClick:ev=>{if(p)return;_setRxW(null);if(v){const r=(ev.currentTarget.closest(`[data-comment-id]`)||ev.currentTarget).querySelector(`.rx-fit.rx-open`);if(r){r.classList.remove(`rx-open`);_rxFit(r)}}y(e=>!e)},",
      'closing the chirp collapses the row')

# --- scrolling lists ---
patch("function _rxWho(ee,only,go,more,wg,nocap){", "const _rxEnd=ev=>{const e=ev.currentTarget;e.classList.toggle(`at-end`,e.scrollTop+e.clientHeight>=e.scrollHeight-2)};\nfunction _rxWho(ee,only,go,more,wg,nocap){", 'scroll-end helper')
patch("const _extra=!nocap&&rows.length>5?rows.length-5:0;if(_extra)rows=rows.slice(0,5);", "const _extra=0;", 'no +N more under a chirp')
patch("(0,L.jsxs)(`div`,{className:`rx-who`,onClick:ev=>ev.stopPropagation(),children:",
      "(0,L.jsxs)(`div`,{className:`rx-who`+(rows.length>5?` rx-scroll`:``),onScroll:_rxEnd,onClick:ev=>ev.stopPropagation(),children:", 'chirp list scrolls')
patch("(0,L.jsx)(`div`,{className:`pr-list`,children:show.map(row)})", "(0,L.jsx)(`div`,{className:`pr-list`+(show.length>5?` rx-scroll`:``),onScroll:_rxEnd,children:show.map(row)})", 'post list scrolls')
patch(":!g.length?(0,L.jsx)(`div`,{className:`cp-empty`,children:`No worms yet`}):\n  g.map(p=>{",
      ":!g.length?(0,L.jsx)(`div`,{className:`cp-empty`,children:`No worms yet`}):(0,L.jsx)(`div`,{className:`pr-list`+(g.length>5?` rx-scroll`:``),onScroll:_rxEnd,children:\n  g.map(p=>{", 'worm list scrolls (open)')
# close the wrapper div after the map: the map ends the Fragment's children with "})]})}" right after
i = c.index("function _WormGivers("); j = c.index("g.map(p=>{", i); k = c.index("},p.username)})]})}", j)
c = c[:k] + "},p.username)})})]})}" + c[k+len("},p.username)})]})}"):]; print('OK: worm list scrolls (close)')

css = ("body .chat-reactions.rx-fit.rx-open{flex-wrap:wrap;row-gap:6px}"
       "body .rx-who.rx-scroll{max-height:156px;overflow-y:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}"
       "body .pr-list.rx-scroll{max-height:260px;overflow-y:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}"
       "body .rx-scroll:not(.at-end){-webkit-mask-image:linear-gradient(to bottom,#000 calc(100% - 34px),transparent);mask-image:linear-gradient(to bottom,#000 calc(100% - 34px),transparent)}"
       "body .rx-scroll{scrollbar-width:none}body .rx-scroll::-webkit-scrollbar{display:none}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
