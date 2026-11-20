#!/usr/bin/env python3
"""Patch v1269 -> v1271 (v1270 was undone): the New Post composer looks like a post card.
The title and the body share one box (same border / radius / background as the box inside feed cards), and the title
placeholder says "Give this post a title…". Huddle mode is unchanged (its invite section sits between title and body)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1269.js'
dst = '_deploy/assets/index-DUcNPOLc-v1271.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("placeholder:_isHuddle?`Give this huddle a title…`:`Give the thread a title…`,disabled:l,style:{",
      "placeholder:_isHuddle?`Give this huddle a title…`:`Give this post a title…`,disabled:l,className:_isHuddle?void 0:`nh-title`,style:{", 'title placeholder + class')
B = "1px solid rgba(148,163,184,.15)"
css = ("body .nh-card .nh-title{display:block;border:" + B + "!important;border-bottom:none!important;border-radius:12px 12px 0 0!important;"
       "background:#1a1d27!important;padding:16px 14px 2px!important;margin:10px 0 0!important;font-size:17px!important;color:#f1f5f9!important}"
       "body .nh-card .nh-title+.nh-msg{border:" + B + "!important;border-top:none!important;border-radius:0 0 12px 12px!important;"
       "background:#1a1d27!important;padding:4px 14px 16px!important;margin-top:0!important}"
       "body .nh-card .nh-title:focus,body .nh-card .nh-title:focus+.nh-msg,body .nh-card .nh-title:has(+.nh-msg:focus),body .nh-card .nh-title+.nh-msg:focus{border-color:#c084fc!important}")
patch("body .lb-ic{", css + "body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
