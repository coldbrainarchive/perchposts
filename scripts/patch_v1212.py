#!/usr/bin/env python3
"""Patch v1211 -> v1212 (try-out): the top fade moves up to the status bar: the picture runs up behind the ✕ and
fades steeply to black just under the time / Dynamic Island (same eased curve as v1211)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1211.js'
dst = '_deploy/assets/index-DUcNPOLc-v1212.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
S = lambda px: f"calc(env(safe-area-inset-top) {'+' if px>=0 else '-'} {abs(px)}px)"
B = lambda px: f"calc(100% - {px}px - env(safe-area-inset-bottom))"
top = ",".join([f"transparent 0", f"transparent {S(-26)}", f"rgba(0,0,0,.08) {S(-21)}", f"rgba(0,0,0,.25) {S(-16)}", f"rgba(0,0,0,.5) {S(-11)}",
                f"rgba(0,0,0,.75) {S(-6)}", f"rgba(0,0,0,.92) {S(-1)}", f"#000 {S(3)}"])
bot = f"#000 {B(66)},rgba(0,0,0,.35) {B(22)},transparent 100%"
g = f"linear-gradient(to bottom,{top},{bot})"
patch("body .lb-ic{", f"body .reel-view{{-webkit-mask-image:{g}!important;mask-image:{g}!important}}body .lb-ic{{", 'fade at the status bar')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
