#!/usr/bin/env python3
"""Patch v1172 -> v1173: the chirp preview's "81 chirps" becomes a pill matching the Highlights dropdown pill
(same height, border, fill, text size and weight). Posts and huddles."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1172.js'
dst = '_deploy/assets/index-DUcNPOLc-v1173.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("body .lb-ic{",
      "body .comments-shell .feed-post-action-pill.cp-count{height:26px;box-sizing:border-box;display:inline-flex;align-items:center;gap:4px;padding:0 10px!important;border:1px solid rgba(148,163,184,.22)!important;background:rgba(148,163,184,.06)!important;border-radius:999px!important;color:#94a3b8;font-size:12px!important;font-weight:700;letter-spacing:normal!important;line-height:1}"
      "body .comments-shell .cp-count .pp-ic svg{width:14px!important;height:14px!important}"
      "body .lb-ic{", 'count pill')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
