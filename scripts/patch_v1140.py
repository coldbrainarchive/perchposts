#!/usr/bin/env python3
"""Patch v1139 -> v1140: post Reactions lists give flaps and worms their own rows. Someone who flapped and gave
worms shows twice on All: a flap row, then a worm row (🪱 N) right below. The Flaps tab shows only flap rows."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1139.js'
dst = '_deploy/assets/index-DUcNPOLc-v1140.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch(" const show=list.filter(p=>tab===`all`||(tab===`flap`&&p.flap));",
      " const show=tab===`all`?list.flatMap(p=>[p.flap?[p,`f`]:null,p.worms?[p,`w`]:null].filter(Boolean)):list.filter(p=>p.flap).map(p=>[p,`f`]);", 'one row per kind')
patch(" const row=p=>{const f=_rxFace(p.username,16),k=f.col;", " const row=([p,kd])=>{const f=_rxFace(p.username,16),k=f.col;", 'row takes a kind')
patch("(0,L.jsxs)(`span`,{className:`pr-did`,children:[p.flap?ic(`BIRD`):null,p.worms?(0,L.jsxs)(`span`,{className:`pr-w`,children:[ic(`WORM`),p.worms]}):null]})]},p.username)};",
      "(0,L.jsx)(`span`,{className:`pr-did`,children:kd===`f`?ic(`BIRD`):(0,L.jsxs)(`span`,{className:`pr-w`,children:[ic(`WORM`),p.worms]})})]},p.username+kd)};", 'row shows one thing')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
