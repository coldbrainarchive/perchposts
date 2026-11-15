#!/usr/bin/env python3
"""Patch v1103 -> v1104: iPhone/iPad Safari had an old padding nudge on post badges (meant for the pin/lock emoji)
that pushed the new line icons right and up. The icon badges now have no padding there either."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1103.js'
dst = '_deploy/assets/index-DUcNPOLc-v1104.js'
c = open(src, encoding='utf-8').read()
old = ".post-badge.pp-badge-ic{color:#fbbf24}"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, ".post-badge.pp-badge-ic{color:#fbbf24;padding:0!important}"); print('OK: no padding nudge on icon badges')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
