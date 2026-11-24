#!/usr/bin/env python3
"""Patch v1357 -> v1358: post chat controls row spread across the width — a labelled filter pill on the left
("≡ All chirps ▾", shows the current filter), Oldest/Newest on the right. The "Showing: … Show all" strip is gone
(the pill says it; All chirps is at the top of its menu). Tighter spacing."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1357.js'
dst = '_deploy/assets/index-DUcNPOLc-v1358.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch('<path d="M4 6h16M7 12h10M10 18h4"/></svg>`}})}',
      '<path d="M4 6h16M7 12h10M10 18h4"/></svg><span class="l">${_CHF[v]}</span><span class="cv">▾</span>`}})}', 'labelled pill')
patch("m.style.right=Math.max(8,innerWidth-r.right)+`px`;",
      "if(r.left<innerWidth/2)m.style.left=Math.max(8,r.left)+`px`;else m.style.right=Math.max(8,innerWidth-r.right)+`px`;", 'menu opens from the left')
patch("{display:`flex`,alignItems:`stretch`,justifyContent:`flex-end`,gap:6,flex:`1 1 100%`}",
      "{display:`flex`,alignItems:`stretch`,justifyContent:`space-between`,gap:6,flex:`1 1 100%`}", 'spread row')
patch("rowGap:_cf&&!c.is_huddle?8:void 0", "rowGap:_cf&&!c.is_huddle?6:void 0", 'tighter')
patch("_cf&&!c.is_huddle&&_cff!==`all`&&(0,L.jsxs)(`div`,{className:`chf-strip`", "!1&&(0,L.jsxs)(`div`,{className:`chf-strip`", 'no strip')
patch("body .lb-ic{",
 "body .ch-ctl .chf-b{width:auto;padding:0 12px 0 10px;gap:6px;font:inherit;font-size:13px;font-weight:800;letter-spacing:.01em;white-space:nowrap}"
 "body .ch-ctl .chf-b svg{width:15px;height:15px;flex-shrink:0}"
 "body .ch-ctl .chf-b .cv{font-size:10px;opacity:.85}"
 "body .chf-b .l,body .chf-b .cv{display:none}body .ch-ctl .chf-b .l,body .ch-ctl .chf-b .cv{display:inline}"
 "body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
