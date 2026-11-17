#!/usr/bin/env python3
"""Patch v1131 -> v1132: worm givers show straight away.
- /worm-counts now returns who gave (g). The worm store keeps it, so the chirp dropdown and the post Reactions
  🪱 tab show names from that cache instead of waiting for /worm-givers. After you give, it refetches once.
- The post page asks for its worm count (and givers) as it loads.
- Giving a worm on a post no longer bumps the bird number for a moment (the bird counts flaps only)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1131.js'
dst = '_deploy/assets/index-DUcNPOLc-v1132.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# store: givers cache
patch("const _ppWorm=(()=>{const cnt=new Map(),mine=new Map(),", "const _ppWorm=(()=>{const gv=new Map(),cnt=new Map(),mine=new Map(),", 'store: givers map')
patch("const K=key(k,id),v=o[id]||{n:0,m:0};if(pend.get(K))continue;cnt.set(K,v.n);mine.set(K,v.m);emit(K)}",
      "const K=key(k,id),v=o[id]||{n:0,m:0};if(pend.get(K))continue;cnt.set(K,v.n);mine.set(K,v.m);gv.set(K,v.g||[]);emit(K)}", 'store: keep givers')
patch("const K=key(k,id),N=Math.max(1,nn||1);\n  cnt.set(K,", "const K=key(k,id),N=Math.max(1,nn||1);gv.delete(K);\n  cnt.set(K,", 'store: giving clears givers')
patch("_ppResp.set(id,{n:o.m?o.n:o.n+1,m:o.m||2})", "_ppResp.set(id,{n:o.n,m:o.m||2})", 'giving no longer bumps the bird')
patch("return{key,want,give,sub,n:K=>cnt.get(K)||0,", "return{key,want,give,sub,g:K=>gv.get(K),setG:(K,v)=>gv.set(K,v),n:K=>cnt.get(K)||0,", 'store: g/setG')

# one loader: cached givers right away; fetch only when not cached (or after a give)
LD = r'''function _wgUse(kind,id,on1){const K=_ppWorm.key(kind,id),[g,set]=(0,_.useState)(()=>_ppWorm.g(K)||null);
 (0,_.useEffect)(()=>{if(!id||!on1)return;let on=!0;const ld=()=>fetch(`${R}/worm-givers?${kind===`c`?`comment_id`:`post_id`}=${encodeURIComponent(id)}`,{headers:er()}).then(r=>r.ok?r.json():{givers:[]}).then(d=>{const v=d.givers||[];_ppWorm.setG(K,v);on&&set(v)}).catch(()=>on&&set(x=>x||[]));
  const c0=_ppWorm.g(K);if(c0)set(c0);else{_ppWorm.want(kind,id);setTimeout(()=>{if(!on)return;const c1=_ppWorm.g(K);c1?set(c1):ld()},250)}
  const u=_ppWorm.sub(K,()=>{const c=_ppWorm.g(K);if(c)set(c);else setTimeout(ld,600)});return()=>{on=!1;u()}},[K,on1]);return g}
'''
i = c.index("function _useWG(cid,on1){"); j = c.index("function _RxWhoC(", i)
c = c[:i] + LD + "function _useWG(cid,on1){return _wgUse(`c`,cid,on1)}\n" + c[j:]; print('OK: chirp givers from cache')
i = c.index("function _WormGivers({kind,id,go,give}){"); j = c.index(" return(0,L.jsxs)(L.Fragment,{children:[give?", i)
c = c[:i] + "function _WormGivers({kind,id,go,give}){const g=_wgUse(kind,id,!0),[op,setOp]=(0,_.useState)(!1);\n" + c[j:]; print('OK: worm tab givers from cache')
# post page loads its worm count + givers up front
patch("function _PostRespLine({id,pv,setCpm}){const ppl=_usePrx(id),[open,setOpen]=(0,_.useState)(!1);",
      "function _PostRespLine({id,pv,setCpm}){const ppl=_usePrx(id),[open,setOpen]=(0,_.useState)(!1);(0,_.useEffect)(()=>{_ppWorm.want(`p`,id)},[id]);", 'post page preloads worms')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
