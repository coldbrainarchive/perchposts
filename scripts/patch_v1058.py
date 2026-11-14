#!/usr/bin/env python3
"""Patch v1057 -> v1058: Share sends only the link. Passing the title as text made iMessage etc. put a separate
text message above the link; the link preview (now per post, from functions/post/[id].js) carries the title."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1057.js'
dst = '_deploy/assets/index-DUcNPOLc-v1058.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('navigator.share({title:c.title,text:c.title,url:t})', 'navigator.share({url:t})', 'post page share')
patch('navigator.share({title:d.title||``,text:d.title||``,url:u})', 'navigator.share({url:u})', 'reel share')
patch('navigator.share({title:e.title,text:e.title,url:n})', 'navigator.share({url:n})', 'card share')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
