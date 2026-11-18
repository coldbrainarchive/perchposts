#!/usr/bin/env python3
"""Patch v1212 -> v1213: the top fade starts right where Safari's own black status strip ends and eases into the
picture over ~36px, so that edge is soft like the bottom (in v1212 the fade sat hidden under Safari's strip)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1212.js'
dst = '_deploy/assets/index-DUcNPOLc-v1213.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
S = lambda px: f"calc(env(safe-area-inset-top) + {px}px)"
B = lambda px: f"calc(100% - {px}px - env(safe-area-inset-bottom))"
top = ",".join(["transparent 0", f"transparent {S(0)}", f"rgba(0,0,0,.06) {S(5)}", f"rgba(0,0,0,.18) {S(10)}", f"rgba(0,0,0,.36) {S(15)}",
                f"rgba(0,0,0,.56) {S(20)}", f"rgba(0,0,0,.75) {S(25)}", f"rgba(0,0,0,.9) {S(30)}", f"#000 {S(36)}"])
bot = f"#000 {B(66)},rgba(0,0,0,.35) {B(22)},transparent 100%"
g = f"linear-gradient(to bottom,{top},{bot})"
patch("body .lb-ic{", f"body .reel-view{{-webkit-mask-image:{g}!important;mask-image:{g}!important}}body .lb-ic{{", 'soft fade below the status strip')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
