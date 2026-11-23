#!/usr/bin/env python3
"""Patch v1315 -> v1316: New Post chips: "+ country" reads "+ region"; it and "+ tag" are the same height (22px) as
the chosen space pill next to them, same text size and caps style, with the dashed outline."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1315.js'
dst = '_deploy/assets/index-DUcNPOLc-v1316.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("!v&&!p&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>x(e=>!e),style:{display:`inline-flex`,alignItems:`center`,gap:3,padding:`2px 8px`,borderRadius:999,border:`1px dashed #3f4756`,background:`none`,color:`#64748b`,fontSize:11,fontWeight:700,cursor:`pointer`},children:`+ country`})",
      "!v&&!p&&(0,L.jsx)(`button`,{type:`button`,className:`utag-add`,onClick:()=>x(e=>!e),children:`+ region`})", 'region chip')
patch("body .utag-add{display:inline-flex;align-items:center;gap:3px;padding:2px 8px;border-radius:999px;border:1px dashed #3f4756;background:none;color:#64748b;font:inherit;font-size:11px;font-weight:700;cursor:pointer}",
      "body .utag-add{display:inline-flex;align-items:center;gap:3px;height:22px;padding:0 9px;box-sizing:border-box;border-radius:999px;border:1px dashed #4b5363;background:none;color:#8b95a7;font:inherit;font-size:10px;font-weight:800;letter-spacing:.03em;text-transform:uppercase;line-height:1;white-space:nowrap;cursor:pointer}", 'chip size')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
