#!/usr/bin/env python3
"""Patch v1322 -> v1323: on New Post, tapping the picked perch tag removes it (fades out), like a picked region or
flock tag; "+ TAG" opens the picker. Caged birds' Cage tag stays put."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1322.js'
dst = '_deploy/assets/index-DUcNPOLc-v1323.js'
c = open(src, encoding='utf-8').read()
old = "oe&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>{p||(x(e=>!e),C(null))},style:{background:`none`,border:`none`,padding:0,cursor:p?`default`:`pointer`},"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "oe&&(0,L.jsx)(`button`,{type:`button`,\"aria-label\":p?void 0:`Remove ${oe.name}`,onClick:ev=>{if(p)return;const el=ev.currentTarget;el.classList.add(`np-out`);x(!1);C(null);setTimeout(()=>g(``),170)},style:{background:`none`,border:`none`,padding:0,cursor:p?`default`:`pointer`},"); print('OK: tap removes perch tag')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
