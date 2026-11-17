#!/usr/bin/env python3
"""Patch v1145 -> v1146: the mod panel's admin "Huddles" tab becomes "Settings", moved to the end of the tabs
(Flock · Archived · Deleted · Bot · Settings). It holds the site switches: Sign-up limit (moved off the Flock tab)
and See all huddles (its title loses the 👥 emoji)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1145.js'
dst = '_deploy/assets/index-DUcNPOLc-v1146.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("..._adm?[[`huddles`,`Huddles`,null],[`bot`,`Bot`,null]]:[]", "..._adm?[[`bot`,`Bot`,null],[`settings`,`Settings`,null]]:[]", 'tab renamed and moved last')
patch("_tb===`flock`&&(0,L.jsx)(_SignupLimit,{},`sul`),_adm&&_tb===`huddles`&&(0,L.jsx)(`div`,{style:{marginTop:16},children:(0,L.jsx)(_HxAdm,{})}),",
      "_adm&&_tb===`settings`&&(0,L.jsxs)(`div`,{className:`set-tab`,children:[(0,L.jsx)(_SignupLimit,{},`sul`),(0,L.jsx)(_HxAdm,{},`hxa`)]}),", 'settings tab content')
patch("children:`👥 See all huddles`}", "children:`See all huddles`}", 'no emoji in the title')
patch("body .lb-ic{", "body .set-tab{margin-top:16px;display:flex;flex-direction:column;gap:12px}body .set-tab .su-lim,body .set-tab .hxa{margin:0}body .su-t{font-weight:800}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
