#!/usr/bin/env python3
"""Patch v846 -> v847: an archived huddle has no Leave button, because nobody can leave it."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v846.js'
dst = '_deploy/assets/index-DUcNPOLc-v847.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
old = 'c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:()=>{const _un3='.replace('`', q)
new = 'c?.is_huddle&&!c.frozen&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:()=>{const _un3='.replace('`', q)
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old)))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
