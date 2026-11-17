#!/usr/bin/env python3
"""Patch v1134 -> v1135: in the preview's Reactions view, the button under the list says "View chirps" instead of
"View all" (which read as if some reactions were hidden)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1134.js'
dst = '_deploy/assets/index-DUcNPOLc-v1135.js'
c = open(src, encoding='utf-8').read()
old = "className:`chat-view-all`,children:_cn?`View all`:`Write the first chirp`"
new = "className:`chat-view-all`,children:_cn?(_cpm===`react`?`View chirps`:`View all`):`Write the first chirp`"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, new); print('OK: label')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
