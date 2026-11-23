#!/usr/bin/env python3
"""Patch v1320 -> v1321: the built-in tags (General, Sports, Science...) are called "Perch tags" in labels:
search dropdown tab + sections, New Post dropdown column + search results."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1320.js'
dst = '_deploy/assets/index-DUcNPOLc-v1321.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("_stb(`boards`,`Tags`)", "_stb(`boards`,`Perch tags`)", 'search tab')
patch("children:[C&&(0,L.jsxs)(`div`,{className:`search-column`,children:[(0,L.jsx)(`div`,{className:`search-section-label`,children:`Tags`})", "children:[C&&(0,L.jsxs)(`div`,{className:`search-column`,children:[(0,L.jsx)(`div`,{className:`search-section-label`,children:`Perch tags`})", 'search results section')
patch("style:{alignContent:`flex-start`},children:[(0,L.jsx)(`div`,{className:`search-section-label`,children:`Tags`})", "style:{alignContent:`flex-start`},children:[(0,L.jsx)(`div`,{className:`search-section-label`,children:`Perch tags`})", 'New Post column')
patch("out.push(lb(`Tags`,`_ltg`))", "out.push(lb(`Perch tags`,`_ltg`))", 'search sections')
patch("...sec(`Tags`,bm.map(", "...sec(`Perch tags`,bm.map(", 'New Post search results')
patch("children:`Tag`}),nr.filter(e=>!e.virtual&&e.slug!==`cage`)", "children:`Perch tag`}),nr.filter(e=>!e.virtual&&e.slug!==`cage`)", 'mod select')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
