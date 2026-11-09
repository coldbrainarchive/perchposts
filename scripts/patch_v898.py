#!/usr/bin/env python3
"""Patch v897 -> v898: keyword search filters the feed live while typing again (user preference).
Undoes v892's "only update the URL once the search box loses focus on phones"; that wasn't the cursor-glitch
cause (v893/v897 fixed it). Kept: Enter on a phone closes the keyboard and the suggestions box, the box stays
open with a "Search posts for" row, and the box is always scroll-ready.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v897.js'
dst = '_deploy/assets/index-DUcNPOLc-v898.js'
content = open(src, encoding='utf-8').read()
old = "if(!(window.matchMedia&&matchMedia(`(pointer:coarse)`).matches&&document.activeElement===c.current)&&(e.get(`q`)||``)!==n.trim()){"
new = "if((e.get(`q`)||``)!==n.trim()){"
if content.count(old) != 1:
    print('FAIL', content.count(old)); sys.exit(1)
content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
