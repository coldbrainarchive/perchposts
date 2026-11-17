#!/usr/bin/env python3
"""Patch v1156 -> v1157: the post page's worm pill number is the same colour as the flap number (it was pink, which
read smaller next to the flap count)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1156.js'
dst = '_deploy/assets/index-DUcNPOLc-v1157.js'
c = open(src, encoding='utf-8').read()
old = "body .lb-ic{"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "body .feed-post-actions .pr-line .pr-w{color:inherit;font-size:inherit;font-weight:inherit}body .lb-ic{", 1); print('OK: same number style')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
