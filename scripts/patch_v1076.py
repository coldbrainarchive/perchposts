#!/usr/bin/env python3
"""Patch v1075 -> v1076: new bird avatars.

Each username gets its own bird, made from the saved Apple emoji in _deploy/birds/ (same on every device):
colour, markings, head feathers and beak all come from the username words (birds/birdkit.js).
  - tags and small spots: the bird cropped to emoji size with a 1px dark outline
  - profile cards, Your Nest and the username picker: the full bird
  - the username tag colour now matches the bird (never mod purple; admins stay white, mods purple)
The plain emoji shows until a bird is drawn. Anonymous names, bots, admins, jailed/banned/extinct keep their old look.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1075.js'
dst = '_deploy/assets/index-DUcNPOLc-v1076.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

kit = ''.join(open('birds/' + f, encoding='utf-8').read() + '\n' for f in ['seg.js', 'birdkit.js', 'runtime.js'])
c = 'const _ppKit=(()=>{const BASE={};let __bk;\n' + kit + 'return{get,sub,tagCol};})();\n' + c

# 1. badge info: named users get their bird instead of the old hue-rotate filter and spots
patch("return{e:_e,f:_f,s:_mkSpots(_a)}}var Yn=",
      "return e.username?{e:_e,f:``,s:null,u:e.username}:{e:_e,f:_f,s:_mkSpots(_a)}}var Yn=", 'badge info')

# 2. the bird component + helper, next to the tag component
patch("function Xn({record:e,name:t,color:n,onClick:r}){",
      "function _PB({n,c,z,k}){const[,_f]=(0,_.useState)(0);const r=_ppKit.get(n,c);(0,_.useEffect)(()=>{if(r)return;const u=_ppKit.sub(n,c,()=>_f(x=>x+1));if(_ppKit.get(n,c))_f(x=>x+1);return u},[n,c,!!r]);"
      "if(!r||r.fail)return c;const w=k===`t`?z*(1+2*r.g):z*2.125;"
      "return(0,L.jsx)(`img`,{src:k===`t`?r.t:r.f,alt:``,draggable:!1,style:{width:w,height:w,margin:-(w-z)/2,display:`block`,maxWidth:`none`,pointerEvents:`none`,flexShrink:0}})}"
      "function _ppB(x,z,k){return x&&x.u&&x.e?(0,L.jsx)(_PB,{n:x.u,c:x.e,z,k},x.u):x&&x.e}"
      "function Xn({record:e,name:t,color:n,onClick:r}){", 'bird component')

# 3. every place a bird shows
patch("children:typeof i===`object`&&i.e?i.e:i}),...(typeof i===`object`&&i.s?_spEls(i.s,14)",
      "children:typeof i===`object`&&i.e?_ppB(i,16,`t`):i}),...(typeof i===`object`&&i.s?_spEls(i.s,14)", 'tag (Xn)')
patch("children:_jd.e||`🐦`}),...(_jd.s?_spEls(_jd.s,13)",
      "children:_jd.e?_ppB(_jd,16,`t`):`🐦`}),...(_jd.s?_spEls(_jd.s,13)", 'small tags', n=5)
patch("children:_bd&&_bd.e?_bd.e:`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,17)",
      "children:_bd&&_bd.e?_ppB(_bd,16,`t`):`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,17)", 'card tag')
patch("children:_bd&&_bd.e?_bd.e:`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,48)",
      "children:_bd&&_bd.e?_ppB(_bd,48,`f`):`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,48)", 'profile card bird')
patch("children:_bird&&_bird.e?_bird.e:`🐤`}),...(_bird&&_bird.s?_spEls(_bird.s,56)",
      "children:_bird&&_bird.e?_ppB(_bird,56,`f`):`🐤`}),...(_bird&&_bird.s?_spEls(_bird.s,56)", 'nest bird')
patch("children:[(0,L.jsx)(`span`,{style:{filter:_f},children:_e}),..._spEls(_sp,40)]",
      "children:[(0,L.jsx)(`span`,{style:{},children:_ppB({e:_e,u:_gu},40,`f`)})]", 'username picker bird')

# 4. tag colour matches the bird
patch("function Hn(e,t){if(t===`Extinct Bird`)return`#9ca3af`;",
      "function Hn(e,t){if(t===`Extinct Bird`)return`#9ca3af`;if(t&&!/^Anon #/.test(t))try{return _ppKit.tagCol(t)}catch(_x){}", 'tag colour')

open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
