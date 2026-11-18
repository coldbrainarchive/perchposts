#!/usr/bin/env python3
"""Patch v1179 -> v1180: board / country / region tags are solid again everywhere (v1178's outline look removed).
The reel keeps reading each tag's colour (--pc), so its tags still show."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1179.js'
dst = '_deploy/assets/index-DUcNPOLc-v1180.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("body .pp-tag{background:transparent!important;color:var(--pc)!important;border:1.5px solid var(--pc)!important;box-sizing:border-box}", "", 'solid tags again')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
