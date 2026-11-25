#!/usr/bin/env python3
"""Patch v1376 -> v1377: /?signin=1 opens the Sign In window (used by the globe page's "Sign in to flap" toast)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1376.js'
dst = '_deploy/assets/index-DUcNPOLc-v1377.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("let e=()=>{Q(!0),setTimeout(()=>Q(!1),2600)};",
      "let e=()=>{Q(!0),setTimeout(()=>Q(!1),2600)};try{const _sq=new URLSearchParams(location.search);if(_sq.get(`signin`)===`1`){_sq.delete(`signin`);history.replaceState(history.state,``,location.pathname+(_sq.toString()?`?`+_sq:``)+location.hash);if(!localStorage.getItem(`auth_token`))setTimeout(()=>d(!0),250)}}catch(_x){};", 'signin=1')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
