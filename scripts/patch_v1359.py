#!/usr/bin/env python3
"""Patch v1358 -> v1359: (built on the v1358 labelled-filter row)
- The ▾ drop-down now fills the whole screen between the header and the message bar (the chirps hide behind it,
  keeping their scroll spot), so videos and long posts get the room.
- Slimmer post header: less padding, smaller back arrow / thumbnail / text."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1358.js'
dst = '_deploy/assets/index-DUcNPOLc-v1359.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch("rowGap:_cf&&!c.is_huddle?6:void 0", "rowGap:_cf&&!c.is_huddle?6:void 0,padding:_cf&&!c.is_huddle?`6px 12px 8px`:void 0", 'header padding')
patch("body .lb-ic{",
 "body .chp.chp-full{max-height:none;flex:1 1 auto;min-height:0;overflow-y:auto;padding-bottom:14px}"
 "body .chp.chp-full~.chat-window{flex:0 0 0px!important;height:0!important;min-height:0!important;padding-top:0!important;padding-bottom:0!important;visibility:hidden}"
 "body .ch-back{width:28px;height:30px;margin-left:-4px}body .ch-back svg{width:20px;height:20px}"
 "body .ch-bar .ch-th{width:30px;height:30px;border-radius:8px}"
 "body:has(.chp-full) .rd-pill{display:none!important}"
 "body .ch-tx{gap:1px}body .ch-t{font-size:14.5px}body .ch-m{font-size:11px}"
 "body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
