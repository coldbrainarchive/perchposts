#!/usr/bin/env python3
"""Patch v1311 -> v1312: tapping a post card opened the scroller with sound forced on ({sound:true}); it now follows
the saved sound setting."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1311.js'
dst = '_deploy/assets/index-DUcNPOLc-v1312.js'
c = open(src, encoding='utf-8').read()
old = "_reelOpen(_cd,{sound:!0})"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "_reelOpen(_cd,{sound:_ppSnd()})"); print('OK')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
