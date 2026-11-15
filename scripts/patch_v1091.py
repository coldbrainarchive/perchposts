#!/usr/bin/env python3
"""Patch v1090 -> v1091: profile card name box.
The admin/mod globe next to the name is drawn black (it vanished on the white or purple fill),
and the name box is shorter (smaller bird space, less padding)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1090.js'
dst = '_deploy/assets/index-DUcNPOLc-v1091.js'
c = open(src, encoding='utf-8').read()
i = c.index('const globe=role?'); j = c.index(':null;', i); g = c[i:j]
if g.count('stroke:k') != 6: print('FAIL globe'); sys.exit(1)
c = c[:i] + g.replace('stroke:k', 'stroke:`#0a0a0a`') + c[j:]; print('OK: black globe')
old = ".bc-card.bc-card .bc-head.bc-rbox{background:var(--rc)!important;border:1.5px solid var(--rc)!important}"
if c.count(old) != 1: print('FAIL fill rule'); sys.exit(1)
c = c.replace(old, old + ".bc-card.bc-card .bc-head.bc-rbox{padding:6px 14px!important}"
                   ".bc-card.bc-card .bc-rbox .bc-av{width:52px!important;height:52px!important}"); print('OK: shorter name box')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
