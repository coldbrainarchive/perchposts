#!/usr/bin/env python3
"""Patch v1187 -> v1188: the profile's "Flaps" tab becomes "Activity": posts the person flapped, fed worms or
chirped on (worker ?activity_by=), newest action first, huddles left out. Each card there gets a small line saying
what they did: "Flapped · 3 chirps · 2 worms · 2h ago"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1187.js'
dst = '_deploy/assets/index-DUcNPOLc-v1188.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("children:`Flaps`})]})})}", "children:`Activity`})]})})}", 'tab says Activity')
patch("`&flapped_by=${encodeURIComponent(l.get(`user`)||p)}`", "`&activity_by=${encodeURIComponent(l.get(`user`)||p)}`", 'fetch activity', n=2)
ACT = r'''function _ActLine({p}){const a=p.act||{},bits=[];const ic=k=>(0,L.jsx)(`span`,{className:`pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(k)}});
 if(a.f)bits.push([`BIRD`,`Flapped`]);if(a.c)bits.push([`CHAT`,a.c===1?`Chirped`:`${a.c} chirps`]);if(a.w)bits.push([`WORM`,`${a.w} worm${a.w===1?``:`s`}`]);
 if(!bits.length)return null;return(0,L.jsxs)(`div`,{className:`pc-act-line`,children:[...bits.map(([k,t],i)=>(0,L.jsxs)(`span`,{className:`pc-act-bit`+(k===`WORM`?` w`:``),children:[ic(k),t]},i)),p.flapped_at?(0,L.jsx)(`span`,{className:`pc-act-when`,children:Un(p.flapped_at)}):null]})}
'''
patch("return(0,L.jsxs)(`div`,{className:`content-card feed-post-card`,style:{marginBottom:16},onClick:_ce=>{if(window.innerWidth>=768&&_ce.target&&!_ce.target.closest(`a,button,video`)){_ce.metaKey||_ce.ctrlKey?window.open(`/post/${e.id}`,`_blank`):_nv(`/post/${e.id}`);}},children:[",
      "return(0,L.jsxs)(`div`,{className:`content-card feed-post-card`,style:{marginBottom:16},onClick:_ce=>{if(window.innerWidth>=768&&_ce.target&&!_ce.target.closest(`a,button,video`)){_ce.metaKey||_ce.ctrlKey?window.open(`/post/${e.id}`,`_blank`):_nv(`/post/${e.id}`);}},children:[e.act&&_pfOn()?(0,L.jsx)(_ActLine,{p:e}):null,", 'card activity line')
patch("function _PFTabs({u,on}){", ACT + "function _pfOn(){try{return new URLSearchParams(location.search).get(`flaps`)===`1`}catch(e){return!1}}\nfunction _PFTabs({u,on}){", 'helpers')
patch("body .lb-ic{",
      "body .pc-act-line{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;margin:-2px 0 12px;padding-bottom:10px;border-bottom:1px solid #262a35;font-size:12px;font-weight:700;color:#c4b5fd}"
      "body .pc-act-bit{display:inline-flex;align-items:center;gap:5px}body .pc-act-bit .pp-ic svg{width:14px!important;height:14px!important}"
      "body .pc-act-bit.w{color:#fda4af}body .pc-act-when{color:#64748b;font-weight:600}body .pc-act-when::before{content:'· '}"
      "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
