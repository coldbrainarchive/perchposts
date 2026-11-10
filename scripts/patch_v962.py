#!/usr/bin/env python3
"""Patch v961 -> v962: unread notifications stand out. Unread pills get a brighter tint, a stronger outline
and a soft glow in the bird's colour; read ones stay faint and slightly dimmed."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v961.js'
dst = '_deploy/assets/index-DUcNPOLc-v962.js'
c = open(src, encoding='utf-8').read()
old = 'background:`color-mix(in srgb, ${c} ${t?16:7}%, #15171d)`,border:`1px solid color-mix(in srgb, ${c} ${t?45:12}%, transparent)`,transition:`background .2s, border-color .2s`}}'
new = ('background:`color-mix(in srgb, ${c} ${t?24:6}%, #15171d)`,border:`1px solid color-mix(in srgb, ${c} ${t?80:10}%, transparent)`,'
       'boxShadow:t?`0 0 0 1px color-mix(in srgb, ${c} 35%, transparent), 0 0 16px color-mix(in srgb, ${c} 45%, transparent)`:`none`,'
       'opacity:t?1:.8,transition:`background .25s, border-color .25s, box-shadow .25s, opacity .25s`}}')
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, new)
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
