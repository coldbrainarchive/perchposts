#!/usr/bin/env python3
"""Patch v857 -> v858: the search bar only touches the address when the search text changed. It used to rewrite
the history entry 300ms after every load, even with nothing to change, which lands right after a swipe back.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v857.js'
dst = '_deploy/assets/index-DUcNPOLc-v858.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
old = 'let e=new URLSearchParams(u.current);n.trim()?e.set(`q`,n.trim()):e.delete(`q`),t(e,{replace:!0});n.trim()?fetch('.replace('`', q)
new = 'let e=new URLSearchParams(u.current);if((e.get(`q`)||``)!==n.trim()){n.trim()?e.set(`q`,n.trim()):e.delete(`q`),t(e,{replace:!0})}n.trim()?fetch('.replace('`', q)
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old)))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
