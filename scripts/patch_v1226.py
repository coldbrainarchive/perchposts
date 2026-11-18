#!/usr/bin/env python3
"""Patch v1225 -> v1226: 📢 Announcements moves from the Tags group to the Spaces group in search
(only admins post there, so it's a space, not a tag)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1225.js'
dst = '_deploy/assets/index-DUcNPOLc-v1226.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const _SPACES=[`activity`,`botnews`,`feedback`,`cage`];",
      "const _SPACES=[`activity`,`botnews`,`announcements`,`feedback`,`cage`];", 'announcements is a space')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
