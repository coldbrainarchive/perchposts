#!/usr/bin/env python3
"""Patch v935 -> v936: send animation text no longer jumps big at landing (user's recording, 0.92s: "Hello"
suddenly grew and slid to the corner). The landing re-applied the chirp's font size and padding from
getComputedStyle(bubble), which is *live*; by landing time the instant chirp had often been swapped for the
server's copy, so the old bubble was gone and the values read back empty (default big text, no padding).
The size and padding are now snapshotted when the flight starts."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v935.js'
dst = '_deploy/assets/index-DUcNPOLc-v936.js'
c = open(src, encoding='utf-8').read()
old = "const tr=bub.getBoundingClientRect(),cs=getComputedStyle(bub),br=body.getBoundingClientRect()"
new = "const tr=bub.getBoundingClientRect(),cs=(_c=>({fontSize:_c.fontSize,padding:_c.padding}))(getComputedStyle(bub)),br=body.getBoundingClientRect()"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, new)
open(dst, 'w', encoding='utf-8').write(c); print('Wrote ' + dst)
