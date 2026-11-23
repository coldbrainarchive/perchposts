#!/usr/bin/env python3
"""Patch v1318 -> v1319: user tags are called "flock tags" (the user base is the Flock): "+ flock tag" chips,
"Flock tags" sections, "Popular flock tags this week", "Blocked flock tags"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1318.js'
dst = '_deploy/assets/index-DUcNPOLc-v1319.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("children:`+ user tag`", "children:`+ flock tag`", 'chips', 2)
patch("...sec(`User tags`,", "...sec(`Flock tags`,", 'New Post results')
patch("children:`Popular tags this week`", "children:`Popular flock tags this week`", 'popular row')
patch("(0,L.jsx)(`div`,{className:`search-section-label`,children:`Tags`}),(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:8,padding:`4px 14px 6px`},children:tags.map(x=>",
      "(0,L.jsx)(`div`,{className:`search-section-label`,children:`Flock tags`}),(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:8,padding:`4px 14px 6px`},children:tags.map(x=>", 'search suggestions')
patch("children:`Blocked tags`}),(0,L.jsx)(`div`,{className:`su-s`,children:`Words nobody can use as a #tag`})", "children:`Blocked flock tags`}),(0,L.jsx)(`div`,{className:`su-s`,children:`Words nobody can use as a flock tag`})", 'settings card')
patch("aria-label\":`Your tag (one word)`", "aria-label\":`Your flock tag (one word)`", 'input label')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
