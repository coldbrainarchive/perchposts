#!/usr/bin/env python3
"""Patch v1344 -> v1345: no double line under the Saved searches block in typed results (the next section's own
divider is hidden when it comes straight after it)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1344.js'
dst = '_deploy/assets/index-DUcNPOLc-v1345.js'
c = open(src, encoding='utf-8').read()
old = "body .lb-ic{"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "body .ss-m+.search-divider{display:none}body .lb-ic{")
open(dst, 'w', encoding='utf-8').write(c); print('OK, wrote', dst)
