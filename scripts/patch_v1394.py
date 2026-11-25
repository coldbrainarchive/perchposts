#!/usr/bin/env python3
"""Patch v1393 -> v1394: notifications that point at a chirp (replies, tags in chirps, new chirps, huddle join/added
lines) jump to it and glow again on the new post / huddle pages. The jump effect ran when the chirps loaded, but the
chat window only exists once the chat view is open (the page shows the loader until then), so it gave up. It now
also re-runs when the chat view opens. (Broken for posts since v1356, for huddles since v1389.)"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1393.js'
dst = '_deploy/assets/index-DUcNPOLc-v1394.js'
c = open(src, encoding='utf-8').read()
old = "if(_b)_glow(_b);});setTimeout(()=>o(`/post/${r}`+(new URLSearchParams(location.search).get(`chat`)===`1`?`?chat=1`:``),{replace:!0}),1800)},[u,a,_nc,_sy]),"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, old.replace("},[u,a,_nc,_sy]),", "},[u,a,_nc,_sy,_cf]),")); print('OK')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
