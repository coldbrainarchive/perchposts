#!/usr/bin/env python3
"""Patch v1124 -> v1125: the list under a tapped chirp shows worm givers too (one row per person: emoji, then 🪱 N),
and shows up even when a chirp has only worms."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1124.js'
dst = '_deploy/assets/index-DUcNPOLc-v1125.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# _rxWho takes worm givers (wg) and merges them into the rows
patch("function _rxWho(ee,only,go,more){let rows=_rxGroup(ee,only);if(!rows.length)return null;",
      "function _rxWho(ee,only,go,more,wg){let rows=_rxGroup(ee,only).map(r=>({...r}));for(const p of wg||[]){const r=rows.find(x=>x.name===p.username);if(r)r.w=p.c;else rows.push({name:p.username,qs:[],w:p.c})}if(!rows.length)return null;",
      'who list takes worm givers')
patch("function _RxAll({ee,cid,go}){",
      r'''function _useWG(cid,on1){const[g,set]=(0,_.useState)(null);
 (0,_.useEffect)(()=>{if(!cid||!on1)return;let on=!0;const ld=()=>fetch(`${R}/worm-givers?comment_id=${encodeURIComponent(cid)}`,{headers:er()}).then(r=>r.ok?r.json():{givers:[]}).then(d=>on&&set(d.givers||[])).catch(()=>on&&set([]));
  ld();const u=_ppWorm.sub(_ppWorm.key(`c`,cid),()=>setTimeout(ld,600));return()=>{on=!1;u()}},[cid,on1]);return g}
function _RxWhoC({ee,cid,go,more}){const wn=_ppWorm.n(_ppWorm.key(`c`,cid)),g=_useWG(cid,wn>0);return _rxWho(ee,null,go,more,wn>0?g:null)}
function _RxAll({ee,cid,go}){''', 'who list component')
patch("v&&ee.length>0&&_rxWho(ee,null,_rxGo,()=>_setRxW(`all`))",
      "v&&(0,L.jsx)(_RxWhoC,{ee,cid:e.id,go:_rxGo,more:()=>_setRxW(`all`)})", 'tapped chirp uses it')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
