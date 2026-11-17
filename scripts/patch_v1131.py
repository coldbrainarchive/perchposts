#!/usr/bin/env python3
"""Patch v1130 -> v1131: the selected chirp pill's purple ring is drawn inside the pill (the reaction row clips
anything outside, which cut off the top of the ring)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1130.js'
dst = '_deploy/assets/index-DUcNPOLc-v1131.js'
c = open(src, encoding='utf-8').read()
old = "body .chat-reaction-pill.sel{border-color:#c084fc!important;background:rgba(192,132,252,.22)!important;box-shadow:0 0 0 1px #c084fc}"
new = "body .chat-reaction-pill.sel{border-color:#c084fc!important;background:rgba(192,132,252,.22)!important;box-shadow:inset 0 0 0 1px #c084fc!important}"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, new); print('OK: ring inside')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
