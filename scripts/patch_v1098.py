#!/usr/bin/env python3
"""Patch v1097 -> v1098: the colour-filled name box (v1089/v1091) is for profile cards only;
the Your Nest card (level box) goes back to its earlier look."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1097.js'
dst = '_deploy/assets/index-DUcNPOLc-v1098.js'
c = open(src, encoding='utf-8').read()
i, j = c.index('/*ppcardfill*/'), c.index('/*/ppcardfill*/')
block = c[i:j]
n = block.count('.bc-card.bc-card ')
if n != 5: print('FAIL', n); sys.exit(1)
c = c[:i] + block.replace('.bc-card.bc-card ', '.bc-card.bc-card:not(.bc-nest) ') + c[j:]; print('OK: fill only on profile cards')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
