#!/usr/bin/env python3
"""Patch v1102 -> v1103: the pin and lock badge icons are bigger (15px, was 12px) and centred in their circles
(the leaning pin is shifted left/down and the lock up, so each drawing's middle sits on the circle's middle)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1102.js'
dst = '_deploy/assets/index-DUcNPOLc-v1103.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('<g transform=\\"rotate(35 12 12)\\">', '<g transform=\\"translate(-1.43 1) rotate(35 12 12)\\">', 'centre the pin')
patch('aria-hidden=\\"true\\"><path d=\\"M8 11V8a4 4 0 0 1 8 0v3\\"/><rect x=\\"5\\" y=\\"11\\" width=\\"14\\" height=\\"10\\" rx=\\"2.5\\"/><path d=\\"M12 15v2.5\\"/></svg>',
      'aria-hidden=\\"true\\"><g transform=\\"translate(0 -.5)\\"><path d=\\"M8 11V8a4 4 0 0 1 8 0v3\\"/><rect x=\\"5\\" y=\\"11\\" width=\\"14\\" height=\\"10\\" rx=\\"2.5\\"/><path d=\\"M12 15v2.5\\"/></g></svg>', 'centre the lock')
patch(".post-badge.pp-badge-ic .ri{width:12px;height:12px;stroke-width:2.3;display:block}", ".post-badge.pp-badge-ic .ri{width:15px;height:15px;stroke-width:2.2;display:block}", 'bigger')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
