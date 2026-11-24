#!/usr/bin/env python3
"""Patch v1361 -> v1362: post chat header without the ‹ back button or the chevron circle — tapping the header
opens / closes the post; leave with the phone's back (swipe / browser back)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1361.js'
dst = '_deploy/assets/index-DUcNPOLc-v1362.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("body .lb-ic{", "body .ch-back,body .ch-cv{display:none!important}body .lb-ic{", 'hide back + chevron')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
