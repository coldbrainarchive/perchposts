#!/usr/bin/env python3
"""Patch v1325 -> v1326: after posting, only admins can add/change/remove a post's flock tag (pencil / + flock tag on
the post page); authors and mods just see the tag."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1325.js'
dst = '_deploy/assets/index-DUcNPOLc-v1326.js'
c = open(src, encoding='utf-8').read()
old = "const canSet=!bot&&!cage&&(mine||adm),canRm=!!tag&&(mine||mod);"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "const canSet=!bot&&!cage&&adm,canRm=!!tag&&adm;"); print('OK: admins only')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
