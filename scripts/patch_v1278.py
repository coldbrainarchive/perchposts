#!/usr/bin/env python3
"""Patch v1277 -> v1278: Visitors is the first mod-panel tab for admins, and the panel opens on it
(mods still open on Flock; ?tab=flagged links still open Flagged)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1277.js'
dst = '_deploy/assets/index-DUcNPOLc-v1278.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("children:[[`flock`,`Flock`,l.length],[`archived`,`Archived`,_archPosts.length],[`deleted`,`Deleted`,d.length],[`flagged`,`Flagged`,null],..._adm?[[`visitors`,`Visitors`,null],[`bot`,`Bot`,null],[`settings`,`Settings`,null]]:[]]",
      "children:[..._adm?[[`visitors`,`Visitors`,null]]:[],[`flock`,`Flock`,l.length],[`archived`,`Archived`,_archPosts.length],[`deleted`,`Deleted`,d.length],[`flagged`,`Flagged`,null],..._adm?[[`bot`,`Bot`,null],[`settings`,`Settings`,null]]:[]]", 'Visitors first')
patch("[_tb,_setTb]=(0,_.useState)(()=>{try{return new URLSearchParams(location.search).get(`tab`)===`flagged`?`flagged`:`flock`}catch(e){return`flock`}})",
      "[_tb,_setTb]=(0,_.useState)(()=>{try{return new URLSearchParams(location.search).get(`tab`)===`flagged`?`flagged`:_adm?`visitors`:`flock`}catch(e){return _adm?`visitors`:`flock`}})", 'admins open on Visitors')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
