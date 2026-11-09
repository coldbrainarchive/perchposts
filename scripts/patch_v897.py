#!/usr/bin/env python3
"""Patch v894 -> v897 (replaces v896): fix the last iPhone search-cursor glitch.
Deleting "et" -> "e" grows the suggestions box from one row to boards + regions + countries (529px of content
in a 392px box), so at that keystroke the box turns into a scrolling panel, and iOS misdraws the cursor
~2 letters right for ~0.2s. A never-scrolling box was clean (v895 experiment, 2/2); v896 (scroll only when
needed) still switched at that keystroke. Here the box is always a scrolling panel while open: an invisible
2px element just below its bottom edge means it always has a little to scroll, so it never switches mode
mid-typing, and long lists still scroll.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v894.js'
dst = '_deploy/assets/index-DUcNPOLc-v897.js'
content = open(src, encoding='utf-8').read()
old = '.search-dropdown {\n        position: absolute;'
new = ('.search-dropdown::after { content: ""; position: absolute; left: 0; top: 100%; width: 1px; height: 2px; pointer-events: none; }\n'
       '      .search-dropdown {\n        position: absolute;')
if content.count(old) != 1:
    print('FAIL', content.count(old)); sys.exit(1)
content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
