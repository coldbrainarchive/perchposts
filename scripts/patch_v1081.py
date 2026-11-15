#!/usr/bin/env python3
"""Patch v1080 -> v1081: parrot beaks get a short, rounded lower half (cut at 62% of the length) so the hooked top hangs over it.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1080.js'
dst = '_deploy/assets/index-DUcNPOLc-v1081.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# 1. updated bird kit (birds/*.js)
head, tail = 'const _ppKit=(()=>{const BASE={};let __bk;\n', 'return{get,sub,tagCol};})();\n'
i, j = c.index(head), c.index(tail) + len(tail)
kit = ''.join(open('birds/' + f, encoding='utf-8').read() + '\n' for f in ['seg.js', 'birdkit.js', 'runtime.js'])
c = c[:i] + head + kit + tail + c[j:]; print('OK: bird kit updated')

open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
