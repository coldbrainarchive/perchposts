#!/usr/bin/env python3
"""Patch v1326 -> v1327: the search dropdown tab is "Tags" again (it shows perch tags and flock tags)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1326.js'
dst = '_deploy/assets/index-DUcNPOLc-v1327.js'
c = open(src, encoding='utf-8').read()
old = "_stb(`boards`,`Perch tags`)"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "_stb(`boards`,`Tags`)"); print('OK')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
