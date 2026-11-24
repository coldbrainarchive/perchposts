#!/usr/bin/env python3
"""Patch v1359 -> v1360: no "View post" links in the post scroller (reel). Posts open in the scroller; the chat
button goes to the chirps (with the ▾ drop-down holding the full post)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1359.js'
dst = '_deploy/assets/index-DUcNPOLc-v1360.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch("if(d.kind===`u`){sn.textContent=`View post`;site.href=`/post/${d.post}`;site.removeAttribute(`target`);site.removeAttribute(`rel`);site.addEventListener(`click`,e=>{e.preventDefault();e.stopPropagation();goPost(d.post)})}else site.addEventListener(`click`,e=>e.stopPropagation());inner.appendChild(site);",
      "if(d.kind!==`u`){site.addEventListener(`click`,e=>e.stopPropagation());inner.appendChild(site)}", 'birds: no View post')
patch("vp.addEventListener(`click`,e=>{e.preventDefault();e.stopPropagation();goPost(d.post)});inner.appendChild(vp)}",
      "}", 'news: no View post')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
