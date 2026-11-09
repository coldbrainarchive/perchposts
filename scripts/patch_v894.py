#!/usr/bin/env python3
"""Patch v893 -> v894: close the suggestions box when the keyword search runs on a phone.
v893 keeps the box open while typing; after pressing Search (or closing the keyboard) its "Search posts for"
row stayed over the results. Now Enter closes it, and on blur it closes if it holds no tag/user suggestions.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v893.js'
dst = '_deploy/assets/index-DUcNPOLc-v894.js'
content = open(src, encoding='utf-8').read()
old = "const v=c.current.value.trim();let e=new URLSearchParams(u.current);"
new = ("const _ud=document.getElementById(`_urd`);if(!_ud||!_ud.querySelector(`.search-suggestion`))a(!1);"
       "const v=c.current.value.trim();let e=new URLSearchParams(u.current);")
old2 = "onKeyDown:e=>{e.key===`Enter`&&window.matchMedia&&matchMedia(`(pointer:coarse)`).matches&&c.current&&c.current.blur(),"
new2 = "onKeyDown:e=>{e.key===`Enter`&&window.matchMedia&&matchMedia(`(pointer:coarse)`).matches&&c.current&&(a(!1),c.current.blur()),"
for o, n, l in [(old, new, 'close on blur'), (old2, new2, 'close on Enter')]:
    if content.count(o) != 1:
        print('FAIL', l, content.count(o)); sys.exit(1)
    content = content.replace(o, n); print('OK:', l)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
