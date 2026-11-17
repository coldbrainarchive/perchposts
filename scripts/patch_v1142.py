#!/usr/bin/env python3
"""Patch v1141 -> v1142: tapping a flap or post-worm notification opens that post with the preview on Reactions,
scrolls to that person's flap row or worm row and makes it glow. Worms on chirps still jump to the chirp.
The link is /post/<id>?rx=f|w&by=<name>."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1141.js'
dst = '_deploy/assets/index-DUcNPOLc-v1142.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# notification link
patch("if(e.type===`vote`)return``;",
      "if(e.type===`vote`||e.type===`worm`)return`?rx=${e.type===`vote`?`f`:`w`}&by=${encodeURIComponent(String(e.text||``).split(` `)[0])}`;",
      'flap/worm notifications link to Reactions')
# post page: ?rx opens Reactions and remembers what to highlight
patch("_setCF(!1);_setCpm(_ppRxOpen.delete(r)?(",
      "_setCF(!1);const _rq=new URLSearchParams(location.search),_rk=_rq.get(`rx`);if(_rk){window._ppRxHL={id:r,k:_rk,u:_rq.get(`by`)||``};history.replaceState(history.state,``,location.pathname)}_setCpm((_ppRxOpen.delete(r)||_rk)?(",
      'post page reads ?rx')
# rows say which kind they are
patch("const row=([p,kd])=>{const f=_rxFace(p.username,16),k=f.col;return(0,L.jsxs)(`div`,{className:`rx-row`,\"data-gpb\":p.username,",
      "const row=([p,kd])=>{const f=_rxFace(p.username,16),k=f.col;return(0,L.jsxs)(`div`,{className:`rx-row`,\"data-gpb\":p.username,\"data-kd\":kd,",
      'rows carry their kind')
# Reactions: find the row and glow it once the list has loaded
patch(" (0,_.useEffect)(()=>{const s=_prxStart.get(id);if(s){_prxStart.delete(id);setTab(s)}});\n",
      " (0,_.useEffect)(()=>{const s=_prxStart.get(id);if(s){_prxStart.delete(id);setTab(s)}});\n const _hlR=(0,_.useRef)(null);\n"
      " (0,_.useEffect)(()=>{const h=window._ppRxHL;if(!h||h.id!==id||!ppl)return;window._ppRxHL=null;setTab(`all`);\n"
      "  setTimeout(()=>{const w=_hlR.current;if(!w)return;const el=[...w.querySelectorAll(`.rx-row[data-kd=\"${h.k}\"]`)].find(x=>x.dataset.gpb===h.u);if(!el)return;\n"
      "   el.scrollIntoView({behavior:`smooth`,block:`center`});el.classList.remove(`pr-hl`,`pr-hl-w`);void el.offsetWidth;el.classList.add(h.k===`w`?`pr-hl-w`:`pr-hl`);setTimeout(()=>el.classList.remove(`pr-hl`,`pr-hl-w`),3200)},500)},[id,ppl]);\n",
      'reactions highlight')
patch("return(0,L.jsxs)(`div`,{className:`pr-wrap`,onClick:ev=>ev.stopPropagation(),children:[",
      "return(0,L.jsxs)(`div`,{className:`pr-wrap`,ref:_hlR,onClick:ev=>ev.stopPropagation(),children:[", 'reactions ref')
css = ("@keyframes prhl{0%,55%{box-shadow:0 0 0 2px #c084fc,0 0 18px rgba(192,132,252,.65)}100%{box-shadow:0 0 0 0 transparent}}"
       "@keyframes prhlw{0%,55%{box-shadow:0 0 0 2px #fb7185,0 0 18px rgba(251,113,133,.6)}100%{box-shadow:0 0 0 0 transparent}}"
       "body .rx-row.pr-hl{animation:prhl 3s ease-out}body .rx-row.pr-hl-w{animation:prhlw 3s ease-out}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
