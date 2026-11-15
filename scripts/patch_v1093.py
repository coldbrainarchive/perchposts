#!/usr/bin/env python3
"""Patch v1092 -> v1093: flycatcher and bee-eater beaks curve down smoothly from the face (no wiggle midway):
the beak is stretched evenly and thins out gradually ("even" beak option in birdkit.js)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1092.js'
dst = '_deploy/assets/index-DUcNPOLc-v1093.js'
c = open(src, encoding='utf-8').read()
head, tail = 'const _ppKit=(()=>{const BASE={};let __bk;\n', 'return{get,sub,tagCol,ready,eye};})();\n'
i, j = c.index(head), c.index(tail) + len(tail)
kit = ''.join(open('birds/' + f, encoding='utf-8').read() + '\n' for f in ['seg.js', 'birdkit.js', 'runtime.js'])
c = c[:i] + head + kit + tail + c[j:]; print('OK: bird kit updated')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
