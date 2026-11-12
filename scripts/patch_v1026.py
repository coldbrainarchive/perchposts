#!/usr/bin/env python3
"""Patch v1025 -> v1026: privacy.
- Link previews (chat box and New Post's link box) come from our own server (/link-preview) instead of
  microlink.io, so no outside company sees which links people type or their IP. Same fields as before.
- YouTube embeds use youtube-nocookie.com (YouTube's privacy-enhanced mode: no tracking cookies until played)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1025.js'
dst = '_deploy/assets/index-DUcNPOLc-v1026.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('fetch(`https://api.microlink.io/?url=${encodeURIComponent(e)}`)', 'fetch(`${R}/link-preview?url=${encodeURIComponent(e)}`,{headers:er()})', 'New Post link box')
patch('fetch(`https://api.microlink.io/?url=${encodeURIComponent(_tu)}`)', 'fetch(`${R}/link-preview?url=${encodeURIComponent(_tu)}`,{headers:er()})', 'chat box')
patch('src:`https://www.youtube.com/embed/${e}`', 'src:`https://www.youtube-nocookie.com/embed/${e}`', 'YouTube without tracking cookies')
if 'microlink' in c: print('FAIL microlink still referenced'); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
