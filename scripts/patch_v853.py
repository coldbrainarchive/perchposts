#!/usr/bin/env python3
"""Patch v852 -> v853: the whole 🤖, antenna and ears included, sits in the middle of its circle, as asked.
A real iPhone close-up measured it 0.47px low with x already centred, so y moves by that much.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v852.js'
dst = '_deploy/assets/index-DUcNPOLc-v853.js'

DESKTOP_Y = sys.argv[1] if len(sys.argv) > 1 else '0.57'
content = open(src, encoding='utf-8').read()
for old, new in (('.post-badge-i{transform:translate(-.25px,-.3px)}', '.post-badge-i{transform:translate(-.25px,-.77px)}'),
                 ('.post-badge-i{display:block;transform:translateY(-.1px)}', '.post-badge-i{display:block;transform:translateY(' + DESKTOP_Y + 'px)}')):
    if content.count(old) != 1:
        print('FAIL: ' + old); sys.exit(1)
    content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
