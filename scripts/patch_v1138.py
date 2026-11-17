#!/usr/bin/env python3
"""Patch v1137 -> v1138: the "Top" icon (key FLAME, used for Top chirps) is a trending-up arrow instead of a flame."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1137.js'
dst = '_deploy/assets/index-DUcNPOLc-v1138.js'
c = open(src, encoding='utf-8').read()
old = '<path d=\\"M12 21.5a6.5 6.5 0 0 0 6.5-6.5c0-3.4-2.2-5.5-3.9-7.6-.4 1.6-1.1 2.6-2 3.1C12.8 7.3 11.4 4.6 9.2 3c.1 2.9-1.3 4.8-2.5 6.4C6.1 10.7 5.5 12.6 5.5 15a6.5 6.5 0 0 0 6.5 6.5z\\"/>'
new = '<path d=\\"M3 17l6-6 4 4 8-8\\"/><path d=\\"M15 7h6v6\\"/>'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, new); print('OK: trending arrow')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
