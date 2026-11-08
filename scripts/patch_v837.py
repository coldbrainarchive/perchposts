#!/usr/bin/env python3
"""Patch v836 -> v837: the Mod Panel's Deleted section becomes Deleted posts, so it can't be mistaken for
the Deleted accounts sort in the Flock.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v836.js'
dst = '_deploy/assets/index-DUcNPOLc-v837.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
old = 'fontWeight:700,flex:1},children:[`Deleted `,'.replace('`', q)
new = 'fontWeight:700,flex:1},children:[`Deleted posts `,'.replace('`', q)
if content.count(old) != 1:
    print('FAIL: expected 1 match, found ' + str(content.count(old)))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
