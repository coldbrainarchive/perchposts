#!/usr/bin/env python3
"""Patch v1099 -> v1100: sharper birds.
Tags are drawn at 2x and big birds (profile cards, Your Nest, the sign-up nest) at 3x, from upscaled copies of the three
Apple emoji (_deploy/birds/*@2x.png, *@3x.png, made once with Real-ESRGAN). Parts are still found on the 160px emoji,
so every bird keeps its exact look. The kit is now a factory: mkKit(SC, BASE) = seg.js (inside, at 160px) + scale.js + birdkit.js.
From v1100 the kit block starts with NEW_HEAD (below) and still ends with TAIL."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1099.js'
dst = '_deploy/assets/index-DUcNPOLc-v1100.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
B = lambda f: open('birds/' + f, encoding='utf-8').read()

# 1. the kit, as a factory for any drawing scale
OLD_HEAD, NEW_HEAD, TAIL = 'const _ppKit=(()=>{const BASE={};let __bk;\n', 'const _ppKit=(()=>{const BASE1={};\n', 'return{get,sub,tagCol,ready,eye};})();\n'
i, j = c.index(OLD_HEAD), c.index(TAIL) + len(TAIL)
kit = ('const mkKit=(SC,BASE)=>{let __bk;\nconst seg1=(()=>{const BASE=BASE1;\n' + B('seg.js') + '\nreturn segment;})();\n'
       + B('scale.js') + '\n' + B('birdkit.js') + '\nreturn __bk;};\n' + B('runtime.js') + '\n')
c = c[:i] + NEW_HEAD + kit + TAIL + c[j:]; print('OK: kit')

# 2. the sign-up nest (birds/nest.js) asks for the big 3x birds
H, T = '/*ppnest*/', '/*/ppnest*/'
a = c.index(H) + len(H); w = c.index('function _PNest(', a)
c = c[:a] + B('nest.js') + '\n' + c[w:]; print('OK: nest')

# 3. the bird component: tags ask for the 2x tag bird, everything else for the 3x big bird
patch("const r=_ppKit.get(n,c);(0,_.useEffect)(()=>{if(r)return;const u=_ppKit.sub(n,c,()=>_f(x=>x+1));if(_ppKit.get(n,c))_f(x=>x+1);return u},[n,c,!!r]);",
      "const kd=k===`t`?`t`:`f`,r=_ppKit.get(n,c,kd);(0,_.useEffect)(()=>{if(r)return;const u=_ppKit.sub(n,c,()=>_f(x=>x+1),kd);if(_ppKit.get(n,c,kd))_f(x=>x+1);return u},[n,c,kd,!!r]);",
      'bird component asks for the right size')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
