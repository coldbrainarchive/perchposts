#!/usr/bin/env python3
"""Patch v1077 -> v1078: cleaner tag outlines.
The outline now ignores faint and hair-thin bits (bristles, soft fades), so it's an even line instead of a smudge,
and the admin bird in tags uses the same drawn outline as everyone else (replacing v1077's blocky CSS shadows)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1077.js'
dst = '_deploy/assets/index-DUcNPOLc-v1078.js'
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

# 2. the bird component can show something else (the plain admin picture) while it's being drawn
patch("function _PB({n,c,z,k}){", "function _PB({n,c,z,k,fb}){", 'component fallback prop')
patch("if(!r||r.fail)return c;const w=", "if(!r||r.fail)return fb!==void 0?fb:c;const w=", 'component fallback')

# 3. admin bird in tags: drawn outline instead of the CSS shadows
OL = ",filter:`drop-shadow(1px 0 0 #0b0c10) drop-shadow(-1px 0 0 #0b0c10) drop-shadow(0 1px 0 #0b0c10) drop-shadow(0 -1px 0 #0b0c10)`"
def admin(style, z, alt, n):
    old = "(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`" + alt + "`,style:{" + style + OL + "}})"
    new = "(0,L.jsx)(_PB,{n:`admin`,c:`A`,z:" + z + ",k:`t`,fb:(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`" + alt + "`,style:{" + style + "}})})"
    patch(old, new, 'admin tag ' + z, n)
admin("height:13,width:13,objectFit:`contain`", "13", "", 5)
admin("height:16,width:16,objectFit:`contain`,display:`block`,flexShrink:0,pointerEvents:`none`", "16", "admin", 1)
admin("height:`17px`,width:`auto`,flexShrink:0,display:`block`", "17", "admin", 1)

open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
