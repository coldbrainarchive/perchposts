#!/usr/bin/env python3
"""Patch v1381 -> v1382: the post row at the top of the chirps sits centred between the phone's clock and the
filter / Oldest-Newest buttons (was 29px above vs 6px below on iPhone). Only shifts where there is a top safe area
(phones), so desktop is unchanged."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1381.js'
dst = '_deploy/assets/index-DUcNPOLc-v1382.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("body .lb-ic{",
 "body .comments-shell.chat-full .chat-panel-header:has(>.ch-bar){row-gap:calc(6px + min(11px, env(safe-area-inset-top,0px)))!important}"
 "body .comments-shell.chat-full .chat-panel-header>.ch-bar{margin-top:calc(-1 * min(11px, env(safe-area-inset-top,0px)))}"
 "body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
