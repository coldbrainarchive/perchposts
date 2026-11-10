#!/usr/bin/env python3
"""Patch v984 -> v985: the post page preview shows the 3 OLDEST pins (oldest at the top), matching the chat's
pinned area order; "+N more pinned" is then the newer pins that follow in the chat."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v984.js'
dst = '_deploy/assets/index-DUcNPOLc-v985.js'
c = open(src, encoding='utf-8').read()
old = 'let _ps=_rev.filter(_x=>_x.pinned).slice(0,3),'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, 'let _ps=_rev.filter(_x=>_x.pinned).slice(-3),')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
