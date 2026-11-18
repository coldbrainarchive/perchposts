#!/usr/bin/env python3
"""Patch v1210 -> v1211: the top fade is one short, steep fade right under the ✕ (black → picture over ~28px with an
eased curve), instead of a long straight ramp whose end showed as a line with a faint tail."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1210.js'
dst = '_deploy/assets/index-DUcNPOLc-v1211.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
S = lambda px: f"calc({px}px + env(safe-area-inset-top))"
B = lambda px: f"calc(100% - {px}px - env(safe-area-inset-bottom))"
top = ",".join([f"transparent 0", f"transparent {S(48)}", f"rgba(0,0,0,.08) {S(53)}", f"rgba(0,0,0,.25) {S(58)}", f"rgba(0,0,0,.5) {S(63)}",
                f"rgba(0,0,0,.75) {S(68)}", f"rgba(0,0,0,.92) {S(73)}", f"#000 {S(77)}"])
bot = f"#000 {B(66)},rgba(0,0,0,.35) {B(22)},transparent 100%"
g = f"linear-gradient(to bottom,{top},{bot})"
patch("body .lb-ic{", f"body .reel-view{{-webkit-mask-image:{g}!important;mask-image:{g}!important}}body .lb-ic{{", 'steep top fade')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
