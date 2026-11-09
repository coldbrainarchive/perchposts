#!/usr/bin/env python3
"""Patch v915 -> v916: in Your Nest for mods/admins, Delete account comes last, after Open Mod Panel."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v915.js'
dst = '_deploy/assets/index-DUcNPOLc-v916.js'
content = open(src, encoding='utf-8').read()
mod = ("(0,L.jsx)(I,{to:`/mod`,onClick:a,style:{display:`block`,padding:`10px 0`,borderRadius:12,lineHeight:`18px`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,cursor:`pointer`,textDecoration:`none`,textAlign:`center`},children:`Open Mod Panel`})")
old = "_dlUi()," + mod + "]})"
new = mod + ",_dlUi()]})"
if content.count(old) != 1: print('FAIL', content.count(old)); sys.exit(1)
content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
