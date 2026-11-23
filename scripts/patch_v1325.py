#!/usr/bin/env python3
"""Patch v1324 -> v1325: New Post regions.
- Region and country buttons hug their pill (were full-width, so the picked outline wrapped the whole row).
- Tapping a region picks it for the post (pill at the top, purple outline) and opens its countries to narrow down;
  a country replaces it at the top (removing the country shows the region again); a different region drops a
  country that isn't in it; tap the region pill to remove it. Sent as continent (when there's no country)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1324.js'
dst = '_deploy/assets/index-DUcNPOLc-v1325.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("borderRadius:999,width:`100%`,justifyContent:`flex-start`", "borderRadius:999,alignSelf:`flex-start`,justifyContent:`flex-start`", 'buttons hug the pill', 2)
patch("function Ur({user:e,userRole:t,memberUsername:n}){let r=nt(),[i]=kn(),", "function Ur({user:e,userRole:t,memberUsername:n}){let r=nt(),[i]=kn(),[_cont,_setCont]=(0,_.useState)(``),", 'region state')
# picking a region (list): select + open its countries
patch("onClick:()=>C(e),style:{outline:`none`,boxShadow:v&&ar[v]===e?`0 0 0 2px #c084fc`:`none`,",
      "onClick:()=>{_setCont(e);if(v&&ar[v]!==e)y(``);C(e)},style:{outline:`none`,boxShadow:(v?ar[v]===e:_cont===e)?`0 0 0 2px #c084fc`:`none`,", 'region pick (list)')
# search results: same, and outline
patch("close:()=>x(!1),pickBoard:g,pickCountry:e=>{y(e);C(null)},pickRegion:e=>C(e),cur:h,curC:v,caged:p",
      "close:()=>x(!1),pickBoard:g,pickCountry:e=>{y(e);if(e)_setCont(ar[e]||``);C(null)},pickRegion:e=>{_setCont(e);if(v&&ar[v]!==e)y(``);C(e)},cur:h,curC:v,curR:_cont,caged:p", 'picker props')
patch("function _NpPicker({close,pickBoard,pickCountry,pickRegion,cur,curC,caged,cols})", "function _NpPicker({close,pickBoard,pickCountry,pickRegion,cur,curC,curR,caged,cols})", 'picker signature')
patch("boxShadow:curC&&ar[curC]===e?`0 0 0 2px #c084fc`:`none`", "boxShadow:(curC?ar[curC]===e:curR===e)?`0 0 0 2px #c084fc`:`none`", 'search region outline')
# picking a country from the lists keeps its region
patch("onClick:()=>{y(e.name===v?``:e.name);C(null);}", "onClick:()=>{if(e.name===v){y(``)}else{y(e.name);_setCont(ar[e.name]||_cont)}C(null);}", 'country keeps region')
# top row: region pill when there's no country
patch("!p&&(0,L.jsx)(_UTagPick,{},`utp`),!p&&(0,L.jsx)(_NpAdd,{hasC:!!v,hasP:!!h,",
      "!v&&_cont&&!p&&(0,L.jsx)(`button`,{type:`button`,\"aria-label\":`Remove ${_cont}`,onClick:ev=>{const el=ev.currentTarget;el.classList.add(`np-out`);setTimeout(()=>_setCont(``),170)},style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(kr,{continent:_cont,small:!0})},`npreg`),!p&&(0,L.jsx)(_UTagPick,{},`utp`),!p&&(0,L.jsx)(_NpAdd,{hasC:!!v||!!_cont,hasP:!!h,", 'region pill')
# send it
patch("continent:null,country:_isHuddle?null:(v||null)", "continent:_isHuddle||v?null:(_cont||null),country:_isHuddle?null:(v||null)", 'send continent')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
