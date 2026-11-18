#!/usr/bin/env python3
"""Patch v1173 -> v1174: chirp section titles (Pinned, Top chirps, Most replied, Latest…) look like the date
dividers: centred small grey uppercase text with a thin line on each side, no pill. A date, when shown, follows
the title ("LATEST · TODAY")."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1173.js'
dst = '_deploy/assets/index-DUcNPOLc-v1174.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
css = ("body .chat-section-title{gap:8px;padding:10px 0;user-select:none}"
       "body .chat-section-title::before{content:'';order:0;flex:1;height:1px;background:rgba(148,163,184,0.12)}"
       "body .chat-section-title .chat-section-pill{order:1;height:auto;padding:0 0 0 10px;border:0;border-radius:0;background:none;color:#475569;font-size:11px;font-weight:600;letter-spacing:.07em}"
       "body .chat-section-title .chat-section-pill .lb-ic,body .chat-section-title .chat-section-pill .pp-ic{color:#475569}"
       "body .chat-section-title .chat-section-pill svg{width:12px!important;height:12px!important}"
       "body .chat-section-title b{order:2}body .chat-section-title b::before{content:'· '}"
       "body .chat-section-title i{order:3;margin-left:10px}")
patch("body .lb-ic{", css + "body .lb-ic{", 'section titles like dates')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
