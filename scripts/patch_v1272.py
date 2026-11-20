#!/usr/bin/env python3
"""Patch v1271 -> v1272: the Huddle composer matches the New Post one.
"Invite birds" moves to the top (CSS order), and the title + opening message share one card-style box.
The separate "Opening message" label is dropped; the placeholder says it's optional and gets pinned."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1271.js'
dst = '_deploy/assets/index-DUcNPOLc-v1272.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("className:_isHuddle?void 0:`nh-title`,", "className:`nh-title`,", 'title box in huddle mode too')
patch("_isHuddle&&(0,L.jsxs)(`div`,{style:{marginTop:6},children:[(0,L.jsx)(`div`,{className:`nh-lb`,children:[`Invite birds`",
      "_isHuddle&&(0,L.jsxs)(`div`,{className:`nh-inv`,style:{marginTop:6},children:[(0,L.jsx)(`div`,{className:`nh-lb`,children:[`Invite birds`", 'invite section class')
patch("_isHuddle&&(0,L.jsx)(`div`,{style:{fontSize:12,color:`#94a3b8`,margin:`14px 0 6px`},className:`nh-lb`,children:[`Opening message`",
      "!1&&(0,L.jsx)(`div`,{style:{fontSize:12,color:`#94a3b8`,margin:`14px 0 6px`},className:`nh-lb`,children:[`Opening message`", 'drop Opening message label')
patch("placeholder:_isHuddle?`Start the conversation…`:", "placeholder:_isHuddle?`Start the conversation (optional, gets pinned)…`:", 'huddle body placeholder')
# sibling selectors: in huddle mode the invite section sits between title and body in the DOM
patch("body .nh-card .nh-title+.nh-msg{", "body .nh-card .nh-title~.nh-msg{", 'css ~ body')
patch("body .nh-card .nh-title:focus,body .nh-card .nh-title:focus+.nh-msg,body .nh-card .nh-title:has(+.nh-msg:focus),body .nh-card .nh-title+.nh-msg:focus{",
      "body .nh-card .nh-title:focus,body .nh-card .nh-title:focus~.nh-msg,body .nh-card .nh-title:has(~.nh-msg:focus),body .nh-card .nh-title~.nh-msg:focus{", 'css ~ focus')
patch("body .lb-ic{", "body .nh-card .feed-post-main:has(>.nh-inv){display:flex;flex-direction:column}body .nh-card .nh-inv{order:-1;margin:0 0 6px!important}body .nh-card .nh-inv>.nh-lb:first-child{margin-top:0!important}body .nh-card input.nh-title{font-size:17px!important;margin-top:10px!important}body .lb-ic{", 'css invite on top')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
