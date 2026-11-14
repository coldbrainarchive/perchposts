#!/usr/bin/env python3
"""Patch v1068 -> v1069: the logo's first move plays 15 seconds after the page loads (was 4), then every 30 seconds after that."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1068.js'
dst = '_deploy/assets/index-DUcNPOLc-v1069.js'
c = open(src, encoding='utf-8').read()
old = 'setTimeout(tick,4000);setInterval(tick,30000);'
new = 'setTimeout(()=>{tick();setInterval(tick,30000)},15000);'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, new); print('OK: first move at 15s')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
