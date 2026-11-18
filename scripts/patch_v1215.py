#!/usr/bin/env python3
"""Patch v1214 -> v1215 (scroller info panel):
- Folded: a single compact row with the title (one line, "…" if too long) and the tags beside it (one line).
  Tapping the title opens the post.
- Unfolded: as before (name, tags, time, title, VIEW POST), but the whole title shows (no 2-line limit)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1214.js'
dst = '_deploy/assets/index-DUcNPOLc-v1215.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("rpan.append(rgrab,rpw,dock);",
      "const rpmw=document.createElement(`div`);rpmw.className=`reel-pmini-w`;const rpm=document.createElement(`div`);rpm.className=`reel-pmini`;rpmw.appendChild(rpm);rpan.append(rgrab,rpmw,rpw,dock);"
      "rpm.addEventListener(`click`,e=>{if(!(e.target.closest&&e.target.closest(`.reel-mt`)))return;e.preventDefault();e.stopPropagation();const o2=slides[i]&&slides[i].querySelector(`a.reel-site`);o2&&o2.click()});", 'compact row container')
patch("rpi.replaceChildren(box);requestAnimationFrame(()=>rpan.classList.add(`open`))};",
      "rpi.replaceChildren(box);"
      "{const mini=document.createElement(`div`);mini.className=`reel-pmini-in`;const mt=document.createElement(`div`);mt.className=`reel-mt`;const tt=s.querySelector(`.reel-title`);mt.textContent=tt?tt.textContent:``;mini.appendChild(mt);"
      "const tg=s.querySelector(`.reel-head .reel-tags`);if(tg){const k=tg.cloneNode(!0);k.removeAttribute(`style`);k.classList.add(`reel-mtags`);mini.appendChild(k)}rpm.replaceChildren(mini)}"
      "requestAnimationFrame(()=>rpan.classList.add(`open`))};", 'build the compact row')
css = ("body .reel-pmini-w{display:grid;grid-template-rows:0fr;transition:grid-template-rows .3s cubic-bezier(.22,.8,.24,1)}"
       "body .reel-panel.open.collapsed .reel-pmini-w{grid-template-rows:1fr}"
       "body .reel-pmini{overflow:hidden;min-height:0}"
       "body .reel-pmini-in{display:flex;align-items:center;gap:10px;padding:2px 12px 10px;border-bottom:1px solid rgba(148,163,184,.3);animation:rpIn .28s ease-out}"
       "body .reel-mt{flex:1 1 auto;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#f1f5f9;font-size:20px;font-weight:800;line-height:1.25;cursor:pointer;text-align:left}"
       "body .reel-pmini-in .reel-mtags{display:flex!important;flex:0 0 auto;flex-wrap:nowrap!important;gap:6px;margin:0!important}"
       "body .reel-pmini-in .reel-mtags .reel-tag{flex:0 0 auto;background:transparent!important}"
       "body .reel-pinfo-in .reel-title{display:block!important;-webkit-line-clamp:unset!important;overflow:visible!important}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
