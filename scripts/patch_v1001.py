#!/usr/bin/env python3
"""Patch v1000 -> v1001: the huddle page's time pill says "4d old" instead of "Started 4d ago" ("New" for a
huddle less than a minute old)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1000.js'
dst = '_deploy/assets/index-DUcNPOLc-v1001.js'
c = open(src, encoding='utf-8').read()
old = 'children:c.is_huddle?`Started ${Un(c.created_at)}`:Un(c.created_at)'
new = 'children:c.is_huddle?(()=>{const _a=Un(c.created_at);return _a===`just now`?`New`:_a.replace(/ ago$/,` old`)})():Un(c.created_at)'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, new); print('OK: old')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
