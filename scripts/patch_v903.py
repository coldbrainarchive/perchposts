#!/usr/bin/env python3
"""Patch v902 -> v903: centre the pills under the Boards | Regions | Filters slider (all three tabs)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v902.js'
dst = '_deploy/assets/index-DUcNPOLc-v903.js'
content = open(src, encoding='utf-8').read()
reps = [
 ('.srch-body { padding: 10px 14px 8px; }', '.srch-body { padding: 10px 14px 8px; justify-content: center; }'),
 ('.srch-row { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 4px; }',
  '.srch-row { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; justify-content: center; margin-bottom: 4px; }'),
]
for o, n in reps:
    if content.count(o) != 1: print('FAIL', o); sys.exit(1)
    content = content.replace(o, n)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
