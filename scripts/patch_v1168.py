#!/usr/bin/env python3
"""Patch v1167 -> v1168: the Members sheet's "Leave" moves up beside "+ Invite", same pill size (red)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1167.js'
dst = '_deploy/assets/index-DUcNPOLc-v1168.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("act&&amIn?(0,L.jsx)(`button`,{type:`button`,className:`hx-addb`+(inv?` on`:``),onClick:ev=>{ev.stopPropagation();setInv(!inv)},children:inv?`Cancel`:`+ Invite`}):null]}),",
      "act&&amIn?(0,L.jsxs)(`span`,{className:`hx-acts`,children:[(0,L.jsx)(`button`,{type:`button`,className:`hx-addb hx-lvb`,onClick:()=>{close();setTimeout(()=>act.leave(),230)},children:`Leave`}),(0,L.jsx)(`button`,{type:`button`,className:`hx-addb`+(inv?` on`:``),onClick:ev=>{ev.stopPropagation();setInv(!inv)},children:inv?`Cancel`:`+ Invite`})]}):null]}),",
      'leave beside invite')
patch(",\n  act&&amIn?(0,L.jsx)(`button`,{type:`button`,className:`hx-leave`,onClick:()=>{close();setTimeout(()=>act.leave(),230)},children:`Leave huddle`}):null]})})}",
      "]})})}", 'no bottom leave')
patch("body .hx-addb{margin-left:auto;", "body .hx-sh .hx-acts{margin-left:auto;display:flex;gap:8px;background:none;padding:0;border-radius:0}body .hx-lvb{border-color:rgba(248,113,113,.4)!important;background:rgba(248,113,113,.08)!important;color:#f87171!important}body .hx-addb{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
