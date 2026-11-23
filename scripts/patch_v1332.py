#!/usr/bin/env python3
"""Patch v1331 -> v1332: feed cards go back to title + link box (no bird text, link description back); the post
scroller keeps the bird's title and text."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1331.js'
dst = '_deploy/assets/index-DUcNPOLc-v1332.js'
c = open(src, encoding='utf-8').read()
old = "_rpOk&&(f||``).trim()?(0,L.jsx)(`div`,{className:`fp-utext`,children:_ppMent((f||``).trim())}):null,(0,L.jsx)(Fr,{attachment:p,postId:e.id,noDesc:_rpOk&&!!(f||``).trim()})]})"
if c.count(old) != 1: print('FAIL'); sys.exit(1)
c = c.replace(old, "(0,L.jsx)(Fr,{attachment:p,postId:e.id})]})"); print('OK: card back to title + link')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
