#!/usr/bin/env python3
"""Patch v901 -> v902: the Boards | Regions | Filters slider is the same height as the pills in the dropdown
(22px, like the board/region chips and the × button beside it), with matching 11px text."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v901.js'
dst = '_deploy/assets/index-DUcNPOLc-v902.js'
content = open(src, encoding='utf-8').read()
reps = [
 ('.srch-tabs { display: flex; margin: 2px 40px 2px; height: 26px;', '.srch-tabs { display: flex; margin: 2px 40px 2px; height: 22px; box-sizing: border-box;'),
 ('.srch-tab { flex: 1; border: none; background: transparent; color: #c084fc; font-size: 12px; font-weight: 700;', '.srch-tab { flex: 1; border: none; background: transparent; color: #c084fc; font-size: 11px; font-weight: 700; line-height: 1;'),
]
for o, n in reps:
    if content.count(o) != 1: print('FAIL', o); sys.exit(1)
    content = content.replace(o, n)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
