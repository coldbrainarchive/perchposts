#!/usr/bin/env python3
"""Patch v1147 -> v1148: post page "A · Flatter" (the user's pick) + a bolder flap icon in Flaps & worms.
- The title/body box loses its border and background (the link preview stays the only box).
- The post's age is plain grey text, not a pill. The chirp count reads "47 chirps" as plain text.
- Flaps & worms: tabs only when the post has both flaps and worms; otherwise just the list. "Give worms" is a pink
  text link.
- The flap icon in Flaps & worms (rows and tabs) is larger and thicker so it sits evenly with the worm."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1147.js'
dst = '_deploy/assets/index-DUcNPOLc-v1148.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("style:c.is_huddle?{padding:`0 2px`,marginBottom:6}:{border:`1px solid rgba(148,163,184,0.15)`,borderRadius:12,background:`#1a1d27`,padding:`14px 16px`,marginBottom:t?10:0}",
      "style:c.is_huddle?{padding:`0 2px`,marginBottom:6}:{padding:`2px 2px 0`,marginBottom:t?10:0}", 'title without a box')
patch("(0,L.jsx)(`span`,{className:`feed-post-action-pill`,style:{marginLeft:`auto`,cursor:`default`},children:c.is_huddle?",
      "(0,L.jsx)(`span`,{className:`feed-post-action-pill pp-time`,style:{marginLeft:`auto`,cursor:`default`},children:c.is_huddle?", 'age as text')
patch("(0,L.jsxs)(`span`,{className:`feed-post-action-pill`,style:{cursor:`default`},\"aria-label\":`${_cn} chirp${_cn===1?``:`s`}`,children:[(0,L.jsx)(`span`,{className:`pp-ic pp-chat`,dangerouslySetInnerHTML:{__html:_ppIco(`CHAT`)}}),(0,L.jsx)(`span`,{children:_cn})]})",
      "(0,L.jsxs)(`span`,{className:`feed-post-action-pill cp-count`,style:{cursor:`default`},\"aria-label\":`${_cn} chirp${_cn===1?``:`s`}`,children:[(0,L.jsx)(`span`,{className:`pp-ic pp-chat`,dangerouslySetInnerHTML:{__html:_ppIco(`CHAT`)}}),(0,L.jsx)(`span`,{children:`${_cn} chirp${_cn===1?``:`s`}`})]})", 'chirp count as text')
# tabs only when both kinds exist
patch(" const show=tab===`all`?", " const _two=nf>0&&nw>0&&!bot,_tb2=_two?tab:`all`;\n const show=_tb2===`all`?", 'effective tab')
patch("tab===`worm`&&!bot?(0,L.jsx)(_WormGivers,", "_tb2===`worm`&&!bot?(0,L.jsx)(_WormGivers,", 'worm list follows it')
patch("(0,L.jsxs)(`div`,{className:`pr-tabs`,children:[T(`all`,`All ${list.length}`),T(`flap`,[ic(`BIRD`),nf]),bot?null:T(`worm`,[ic(`WORM`),nw]),",
      "(0,L.jsxs)(`div`,{className:`pr-tabs`+(_two?``:` pr-notabs`),children:[..._two?[T(`all`,`All ${list.length}`),T(`flap`,[ic(`BIRD`),nf]),T(`worm`,[ic(`WORM`),nw])]:[],", 'tabs only when useful')
css = ("body .feed-post-action-pill.pp-time,body .feed-post-action-pill.cp-count{border:0!important;background:none!important;padding:0 2px!important;box-shadow:none!important}"
       "body .feed-post-action-pill.pp-time{color:#64748b!important;font-weight:600}body .feed-post-action-pill.cp-count{color:#94a3b8!important}"
       "body .pr-tabs .wg-open{border:0;background:none;padding:0 4px;height:auto;color:#fda4af}body .pr-tabs .wg-open:hover{color:#fecdd3}"
       "body .pr-tabs.pr-notabs{justify-content:flex-end;margin-bottom:6px}body .pr-tabs:empty{display:none}"
       "body .pr-wrap .pr-did svg.ri,body .pr-wrap .pr-tab svg.ri{width:22px!important;height:22px!important;stroke-width:2.7}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
