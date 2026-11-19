#!/usr/bin/env python3
"""Patch v1241 -> v1242: caged birds don't see what they can't use.
- New post page: no POST/HUDDLE switch (always a post) and no + photos/video button. The link button stays.
- Post page chirp box: no + photo/video button.
- The post page now checks The Cage by account as well as by device (before, only the device that was caged)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1241.js'
dst = '_deploy/assets/index-DUcNPOLc-v1242.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("children:[(0,L.jsxs)(`div`,{className:`sort-toggle`,style:{width:`fit-content`},children:[(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn`:`sort-toggle-btn active`",
      "children:[!p&&(0,L.jsxs)(`div`,{className:`sort-toggle`,style:{width:`fit-content`},children:[(0,L.jsx)(`button`,{type:`button`,className:_isHuddle?`sort-toggle-btn`:`sort-toggle-btn active`",
      'no Post/Huddle switch when caged')
patch(".jailed?(m(!0),g(`cage`),localStorage.setItem(`_caged`,`1`))",
      ".jailed?(m(!0),g(`cage`),_setIsHuddle(!1),localStorage.setItem(`_caged`,`1`))",
      'caged: always a post, even from a Huddle link')
patch("children:[(0,L.jsx)(`button`,{type:`button`,className:`np-tool`+(_hm||ne?` on`:``)",
      "children:[p?null:(0,L.jsx)(`button`,{type:`button`,className:`np-tool`+(_hm||ne?` on`:``)",
      'no + media button on new post when caged')
patch("children:[(0,L.jsx)(`button`,{type:`button`,onClick:()=>{if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}_cMR.current?.click()}",
      "children:[oe?null:(0,L.jsx)(`button`,{type:`button`,onClick:()=>{if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}_cMR.current?.click()}",
      'no + media button in the chirp box when caged')
patch("fetch(`${R}/check-jailed?browser_id=${_bid}`).then(e=>e.json()).then(e=>{e.jailed&&se(!0)})",
      "fetch(`${R}/check-jailed?browser_id=${_bid}`+(Qn()?.username?`&username=${encodeURIComponent(Qn().username)}`:``)).then(e=>e.json()).then(e=>{e.jailed&&se(!0)})",
      'post page knows a caged account on any device')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
