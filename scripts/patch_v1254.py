#!/usr/bin/env python3
"""Patch v1253 -> v1254: Perch News's tag icon is the black-lined globe that mods and admins carry on their
bird pill (same drawing), instead of the dark-filled site logo with purple lines."""
import sys, re
src = '_deploy/assets/index-DUcNPOLc-v1253.js'
dst = '_deploy/assets/index-DUcNPOLc-v1254.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
i = c.find("n.slug===`botnews`?(0,L.jsx)(`span`,{className:`pp-pn-ic`")
j = c.find("}}):(0,L.jsx)(`span`,{style:{display:`flex`", i)
old = c[i:j+4]
G = ('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs><clipPath id="pnbcc"><circle cx="50" cy="50" r="44"/></clipPath></defs>'
     '<g fill="none" stroke="#0a0a0a"><circle cx="50" cy="50" r="44" stroke-width="7"/><line x1="6" y1="50" x2="94" y2="50" stroke-width="6"/>'
     '<path d="M 14 28 Q 50 38 86 28" stroke-width="6"/><path d="M 14 72 Q 50 62 86 72" stroke-width="6"/>'
     '<ellipse cx="50" cy="50" rx="16" ry="44" stroke-width="6" clip-path="url(#pnbcc)"/><ellipse cx="50" cy="50" rx="32" ry="44" stroke-width="6" clip-path="url(#pnbcc)"/></g></svg>')
patch(old, "n.slug===`botnews`?(0,L.jsx)(`span`,{className:`pp-pn-ic2`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:`" + G + "`}}):", 'Perch News = mod globe')
patch("body .lb-ic{", "body .pp-pn-ic2{display:inline-flex;width:14px;height:14px;flex-shrink:0}body .pp-pn-ic2 svg{width:100%;height:100%;display:block}body .lb-ic{", 'globe size')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
