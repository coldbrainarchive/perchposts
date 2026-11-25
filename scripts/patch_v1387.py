#!/usr/bin/env python3
"""Patch v1386 -> v1387: "Pinned" in the chirp filter drop-down (shows only pinned chirps, newest first).
Pinned chirps always come with the chat (worker loads them all), so nothing extra to fetch."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1386.js'
dst = '_deploy/assets/index-DUcNPOLc-v1387.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("const _CHF={all:`All chirps`,top:`Top`,rep:`Most replied`,media:`Media`,react:`Flaps`};",
      "const _CHF={all:`All chirps`,top:`Top`,rep:`Most replied`,media:`Media`,pin:`Pinned`,react:`Flaps`};", 'label')
patch("media:SV(`<rect x=\"3.5\" y=\"4.5\" width=\"17\" height=\"15\" rx=\"2.5\"/><circle cx=\"9\" cy=\"10\" r=\"1.6\"/><path d=\"m20.5 16-5-5-8.5 8.5\"/>`),react:_ppIco(`BIRD`)};",
      "media:SV(`<rect x=\"3.5\" y=\"4.5\" width=\"17\" height=\"15\" rx=\"2.5\"/><circle cx=\"9\" cy=\"10\" r=\"1.6\"/><path d=\"m20.5 16-5-5-8.5 8.5\"/>`),pin:_ppIco(`PIN`),react:_ppIco(`BIRD`)};", 'icon')
patch("_cff===`media`?_rev.filter(_x=>/\\[ATTACH/.test(_x.content||``)):[];",
      "_cff===`media`?_rev.filter(_x=>/\\[ATTACH/.test(_x.content||``)):_cff===`pin`?_rev.filter(_x=>_x.pinned):[];", 'filter')
patch("const _CPE={top:`No reactions yet`,", "const _CPE={pin:`No pinned chirps yet`,top:`No reactions yet`,", 'empty text')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
