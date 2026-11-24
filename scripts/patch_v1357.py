#!/usr/bin/env python3
"""Patch v1356 -> v1357: post chat header — the post (back, thumbnail, title, bird/site, chirps, ▾) spans the whole
top row; the filter button + Oldest/Newest sit on a row below it, the filter the same height as the toggle.
While the ▾ drop-down is open that row hides. Huddles unchanged."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1356.js'
dst = '_deploy/assets/index-DUcNPOLc-v1357.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch("(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:6,flexShrink:0},children:[_cf&&!c.is_huddle&&(0,L.jsx)(_ChFilter,",
      "(0,L.jsxs)(`div`,{className:_cf&&!c.is_huddle?`ch-ctl`+(_chx?` off`:``):void 0,style:_cf&&!c.is_huddle?{display:`flex`,alignItems:`stretch`,justifyContent:`flex-end`,gap:6,flex:`1 1 100%`}:{display:`flex`,alignItems:`center`,gap:6,flexShrink:0},children:[_cf&&!c.is_huddle&&(0,L.jsx)(_ChFilter,", 'controls row')
patch("(0,L.jsxs)(`div`,{className:`chat-panel-header`,style:{display:`flex`,alignItems:`center`,justifyContent:`space-between`}",
      "(0,L.jsxs)(`div`,{className:`chat-panel-header`,style:{display:`flex`,alignItems:`center`,justifyContent:`space-between`,flexWrap:_cf&&!c.is_huddle?`wrap`:void 0,rowGap:_cf&&!c.is_huddle?8:void 0}", 'header wraps')
patch("onClick:_cf?(c.is_huddle?_closeC:()=>_setChx(v=>!v)):void 0,style:{display:`flex`,alignItems:`center`,gap:8,minWidth:0}",
      "onClick:_cf?(c.is_huddle?_closeC:()=>_setChx(v=>!v)):void 0,style:{display:`flex`,alignItems:`center`,gap:8,minWidth:0,flex:_cf&&!c.is_huddle?`1 1 100%`:void 0}", 'bar full row')
patch("body .lb-ic{",
 "body .ch-ctl.off{display:none!important}"
 "body .ch-ctl .chf-b{height:auto;width:44px;align-self:stretch}"
 "body .ch-ctl .chf-b svg{width:16px;height:16px}"
 "body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
