#!/usr/bin/env python3
"""Patch v1004 -> v1005: Mod Panel gets a Huddles tab (admins only, next to Bot) holding the "See all huddles"
switch, instead of the switch sitting above the tabs."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1004.js'
dst = '_deploy/assets/index-DUcNPOLc-v1005.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('_adm&&(0,L.jsx)(_HxAdm,{}),', '', 'switch off the top')
patch('..._adm?[[`bot`,`Bot`,null]]:[]', '..._adm?[[`huddles`,`Huddles`,null],[`bot`,`Bot`,null]]:[]', 'Huddles tab')
patch('},_k))}),(()=>{let t=[...se.trim()',
      '},_k))}),_adm&&_tb===`huddles`&&(0,L.jsx)(`div`,{style:{marginTop:16},children:(0,L.jsx)(_HxAdm,{})}),(()=>{let t=[...se.trim()',
      'switch in the tab')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
