#!/usr/bin/env python3
"""Patch v948 -> v949: the post's creator (OP) can pin/unpin their own chirps on their own post (any post,
not just huddles). Uses /pin-huddle-comment, which now allows that for any post (own chirps only)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v948.js'
dst = '_deploy/assets/index-DUcNPOLc-v949.js'
c = open(src, encoding='utf-8').read()
old = '||(c.is_huddle&&n&&c.username&&n.toLowerCase()===c.username.toLowerCase()&&_e.username&&_e.username.toLowerCase()===n.toLowerCase())),onPin:'
new = '||(n&&c.username&&n.toLowerCase()===c.username.toLowerCase()&&_e.username&&_e.username.toLowerCase()===n.toLowerCase())),onPin:'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, new)
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
