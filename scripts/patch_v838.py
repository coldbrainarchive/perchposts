#!/usr/bin/env python3
"""Patch v837 -> v838: only the admin sees the Delete button on members. Mods can still cage and ban."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v837.js'
dst = '_deploy/assets/index-DUcNPOLc-v838.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
old = '!d&&(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Delete ${i||`this flock member`}?'.replace('`', q)
new = 'e&&!d&&(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Delete ${i||`this flock member`}?'.replace('`', q)
if content.count(old) != 1:
    print('FAIL: expected 1 match, found ' + str(content.count(old)))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
