#!/usr/bin/env python3
"""Patch v1209 -> v1210: the "Swipe up for the next post" hint shows only on the first post and is gone after the
first swipe (v1209's alignment rule forced it visible). The end-of-list "You're all caught up" still shows."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1209.js'
dst = '_deploy/assets/index-DUcNPOLc-v1210.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("hint.style.display=swiped&&!(last&&ended)?`none`:``;", "hint.classList.toggle(`gone`,swiped&&!(last&&ended));", 'hide by class')
patch("body .lb-ic{", "body .reel .reel-hint.gone{display:none!important}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
