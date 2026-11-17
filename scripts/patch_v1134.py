#!/usr/bin/env python3
"""Patch v1133 -> v1134: chirps work like the phone at every screen size.
- Tapping the chirp preview (or View all, or a ?chat=1 link) opens the full-screen chat on computers too, with the
  phone React sheet (chirp lifted above the emoji). Before, computers showed the chat inside the page instead.
- On wide screens the full-screen chat sits in the site's centred 680px column instead of stretching edge to edge."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1133.js'
dst = '_deploy/assets/index-DUcNPOLc-v1134.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("let _openC=()=>{if(_cf)return;if(window.innerWidth>=768){o(location.pathname+`?chat=1`);return}", "let _openC=()=>{if(_cf)return;", 'full-screen chat on every size')
patch("if(window.innerWidth<768&&(a||_nc||_sy||_first&&te.current))_openC()", "if(a||_nc||_sy||_first&&te.current)_openC()", 'chat links open full screen on every size')
patch("if(!(window.matchMedia&&matchMedia(`(max-width: 900px)`).matches)){history.replaceState(history.state,``,location.pathname);return}", "", 'computers keep ?chat=1')
patch("let _pv=!_cf&&!(window.innerWidth>=768&&new URLSearchParams(location.search).get(`chat`)===`1`)&&", "let _pv=!_cf&&", 'preview rule same everywhere')
patch("body .lb-ic{", "@media (min-width:768px){body .comments-shell.chat-full{left:max(0px,calc(50% - 340px));right:max(0px,calc(50% - 340px));border-left:1px solid #23252e;border-right:1px solid #23252e}}body .lb-ic{", 'centred column on wide screens')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
