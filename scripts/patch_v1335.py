#!/usr/bin/env python3
"""Patch v1334 -> v1335: "tagged you in a post" notifications open the post page at the top
(no ?nc= jump to the chirps). Tags in chirps still jump to that chirp (?highlight=)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1334.js'
dst = '_deploy/assets/index-DUcNPOLc-v1335.js'
c = open(src, encoding='utf-8').read()
old = "let _t=e.text||'';let _m=_t.match(/(?:invited|added|removed)\\s+(\\S+)/);"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, "let _t=e.text||'';if(e.icon===`AT`&&!e.targetId)return '';let _m=_t.match(/(?:invited|added|removed)\\s+(\\S+)/);"); print('OK')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
