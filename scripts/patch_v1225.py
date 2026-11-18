#!/usr/bin/env python3
"""Patch v1224 -> v1225: two new stock tags, 🌿 Nature (slug nature, green) and 🎬 Entertainment (slug entertainment,
rose). Science (science-nature) moves from green to teal so it doesn't look like Nature. They show up wherever tags
do (cards, post page, search Tags tab, new-post picker)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1224.js'
dst = '_deploy/assets/index-DUcNPOLc-v1225.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("{name:`Science`,slug:`science-nature`,icon:`🔬`},",
      "{name:`Science`,slug:`science-nature`,icon:`🔬`},{name:`Nature`,slug:`nature`,icon:`🌿`},{name:`Entertainment`,slug:`entertainment`,icon:`🎬`},", 'tag list')
patch("\"science-nature\":`#4ade80`,", "\"science-nature\":`#2dd4bf`,nature:`#4ade80`,entertainment:`#fb7185`,", 'colours')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
