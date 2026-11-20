#!/usr/bin/env python3
"""Patch v1286 -> v1287: link posts in the post scroller: the site link moves up between the title and the text,
and a "View post" link (like birds' posts have) goes where the site link was, opening the post page."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1286.js'
dst = '_deploy/assets/index-DUcNPOLc-v1287.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("inner.appendChild(site);",
      "inner.appendChild(site);if(d.kind!==`u`&&d.post){const tt=inner.querySelector(`.reel-title`);if(tt){tt.after(site);site.classList.add(`reel-site-up`)}"
      "const vp=document.createElement(`a`);vp.className=`reel-site reel-vp`;vp.href=`/post/${d.post}`;const vs=document.createElement(`span`);vs.textContent=`View post`;const va=document.createElement(`span`);va.className=`reel-site-ar`;va.innerHTML=_RI.ARROW;vp.append(vs,va);"
      "vp.addEventListener(`click`,e=>{e.preventDefault();e.stopPropagation();goPost(d.post)});inner.appendChild(vp)}", 'site link up + View post')
patch("body .lb-ic{", "body .reel-site-up{margin-top:8px}body .reel-site-up+.reel-descw,body .reel-site-up+.reel-desc{margin-top:10px}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
