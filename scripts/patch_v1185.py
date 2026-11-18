#!/usr/bin/env python3
"""Patch v1184 -> v1185: Spaces order is Flock · Huddles · Bot News · The Cage."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1184.js'
dst = '_deploy/assets/index-DUcNPOLc-v1185.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("{name:`Bot News`,slug:`botnews`,icon:`🤖`,virtual:!0},{name:`Huddles`,slug:`feedback`,icon:`👥`},",
      "{name:`Huddles`,slug:`feedback`,icon:`👥`},{name:`Bot News`,slug:`botnews`,icon:`🤖`,virtual:!0},", 'list order')
patch("const _SPACES=[`activity`,`botnews`,`feedback`,`cage`];", "const _SPACES=[`activity`,`feedback`,`botnews`,`cage`];", 'spaces order')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
