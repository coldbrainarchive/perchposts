#!/usr/bin/env python3
"""Patch v914 -> v915: while typing, the search dropdown's matches stack as sections (Boards, Regions,
Countries, Users) instead of two side-by-side columns. The two-column grid stretched the shorter column to
the taller one's height and spread its few pills out, leaving big gaps (e.g. a lone SCIENCE far below its
BOARDS label). Each section is now only as tall as its matches, label and pills centred, with a divider
between sections. Scoped to the search dropdown (#_urd); the New Post picker keeps its columns."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v914.js'
dst = '_deploy/assets/index-DUcNPOLc-v915.js'
content = open(src, encoding='utf-8').read()
old = '.search-divider { height: 1px; background: #374151; margin: 8px 0; }'
new = (old + '\n'
       '      #_urd .search-columns { display: flex; flex-direction: column; }\n'
       '      #_urd .search-columns .search-column { border-right: none; justify-content: center; align-content: flex-start; padding: 6px 14px 8px; }\n'
       '      #_urd .search-columns .search-column + .search-column { border-top: 1px solid #374151; padding-top: 10px; }\n'
       '      #_urd .search-section-label { text-align: center; }\n'
       '      #_urd div[style*="flex-wrap: wrap"] { justify-content: center; }')
if content.count(old) != 1: print('FAIL', content.count(old)); sys.exit(1)
content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
