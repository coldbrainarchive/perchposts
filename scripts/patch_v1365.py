#!/usr/bin/env python3
"""Patch v1364 -> v1365: the chat header's bird name uses the same colours as the name pills — admins white,
mods purple, everyone else their bird colour."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1364.js'
dst = '_deploy/assets/index-DUcNPOLc-v1365.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("(0,L.jsx)(`span`,{style:{color:Hn(post.browser_id,post.username),fontWeight:800},children:post.username})",
      "(0,L.jsx)(`span`,{style:{color:_chNameCol(post),fontWeight:800},children:post.username})", 'name colour')
c += "\nfunction _chNameCol(p){try{const i=Jn(p);if(p.is_admin===!0||p.is_admin===1||(i&&i.hat))return`#ffffff`;if(qn(p))return`#c084fc`}catch(e){}return Hn(p.browser_id,p.username)}\n"
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
