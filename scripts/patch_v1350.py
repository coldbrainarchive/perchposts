#!/usr/bin/env python3
"""Patch v1349 -> v1350: the globe logo's radar pulse is centred on the globe drawing (which sits 55.5% across /
52.7% down the logo box, 72.7% wide), and the red "new stories" dot moves to the top-left."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1349.js'
dst = '_deploy/assets/index-DUcNPOLc-v1350.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch('html.gl-new .pp-logo::after{content:"";position:absolute;top:1px;right:0;',
      'html.gl-new .pp-logo::after{content:"";position:absolute;top:1px;left:0;', 'dot left')
patch('html.gl-new .pp-logo::before{content:"";position:absolute;inset:3px;',
      'html.gl-new .pp-logo::before{content:"";position:absolute;left:19.1%;top:16.3%;width:72.7%;height:72.7%;box-sizing:border-box;', 'pulse centred')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
