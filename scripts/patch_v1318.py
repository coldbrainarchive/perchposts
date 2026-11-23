#!/usr/bin/env python3
"""Patch v1317 -> v1318: the "+ tag" chips (New Post and post page) read "+ user tag"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1317.js'
dst = '_deploy/assets/index-DUcNPOLc-v1318.js'
c = open(src, encoding='utf-8').read()
old = "className:`utag-add`,onClick:()=>setEd(!0),children:`+ tag`"
if c.count(old) != 2: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "className:`utag-add`,onClick:()=>setEd(!0),children:`+ user tag`"); print('OK: both chips')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
