#!/usr/bin/env python3
"""Patch v1158 -> v1159: the post page's age ("11d ago") is a pill again, the same as on feed cards."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1158.js'
dst = '_deploy/assets/index-DUcNPOLc-v1159.js'
c = open(src, encoding='utf-8').read()
old = "body .feed-post-action-pill.pp-time,body .feed-post-action-pill.cp-count{border:0!important;background:none!important;padding:0 2px!important;box-shadow:none!important}body .feed-post-action-pill.pp-time{color:#64748b!important;font-weight:600}"
new = "body .feed-post-action-pill.cp-count{border:0!important;background:none!important;padding:0 2px!important;box-shadow:none!important}"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, new); print('OK: age pill back')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
