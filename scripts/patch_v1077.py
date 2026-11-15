#!/usr/bin/env python3
"""Patch v1076 -> v1077: no more beard trait (bibbed names get a bib, barbets/puffbirds get bristles),
and the admin bird in tags gets the same 1px dark outline as everyone's bird."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1076.js'
dst = '_deploy/assets/index-DUcNPOLc-v1077.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# 1. swap in the updated bird kit (birds/*.js)
head, tail = 'const _ppKit=(()=>{const BASE={};let __bk;\n', 'return{get,sub,tagCol};})();\n'
i, j = c.index(head), c.index(tail) + len(tail)
kit = ''.join(open('birds/' + f, encoding='utf-8').read() + '\n' for f in ['seg.js', 'birdkit.js', 'runtime.js'])
c = c[:i] + head + kit + tail + c[j:]; print('OK: bird kit updated')

# 2. admin bird in tags: 1px dark outline, like the other birds
OL = ",filter:`drop-shadow(1px 0 0 #0b0c10) drop-shadow(-1px 0 0 #0b0c10) drop-shadow(0 1px 0 #0b0c10) drop-shadow(0 -1px 0 #0b0c10)`"
patch("src:`/admin-bird.png`,alt:``,style:{height:13,width:13,objectFit:`contain`}",
      "src:`/admin-bird.png`,alt:``,style:{height:13,width:13,objectFit:`contain`" + OL + "}", 'admin small tags', n=5)
patch("src:`/admin-bird.png`,alt:`admin`,style:{height:16,width:16,objectFit:`contain`,display:`block`,flexShrink:0,pointerEvents:`none`}",
      "src:`/admin-bird.png`,alt:`admin`,style:{height:16,width:16,objectFit:`contain`,display:`block`,flexShrink:0,pointerEvents:`none`" + OL + "}", 'admin tag')
patch("src:`/admin-bird.png`,alt:`admin`,style:{height:`17px`,width:`auto`,flexShrink:0,display:`block`}",
      "src:`/admin-bird.png`,alt:`admin`,style:{height:`17px`,width:`auto`,flexShrink:0,display:`block`" + OL + "}", 'admin card tag')

open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
