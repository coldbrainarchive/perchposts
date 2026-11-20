#!/usr/bin/env python3
"""Patch v1276 -> v1277: Visitors tab calendar. The Today box gets a date picker (back to the first recorded day);
it then shows that day's members by name and guest count. Tapping a day in the 14-day list picks it too."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1276.js'
dst = '_deploy/assets/index-DUcNPOLc-v1277.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("[by,setBy]=(0,_.useState)(`day`);", "[by,setBy]=(0,_.useState)(`day`),[on,setOn]=(0,_.useState)(``);", 'picked day state')
patch("${by!==`day`?`&by=${by}`:``}`", "${by!==`day`?`&by=${by}`:``}${on?`&on=${on}`:``}`", 'fetch picked day')
patch("},[hide,by]);", "},[hide,by,on]);", 'refetch on pick')
TD = "(0,L.jsx)(`div`,{className:`vis-h`,children:`Today`})"
patch(TD,
      "(0,L.jsxs)(`div`,{className:`vis-h vis-hs`,children:[on&&on!==_ppLD()?fd(on):`Today`,(0,L.jsxs)(`span`,{className:`vis-by`,children:[on&&on!==_ppLD()?(0,L.jsx)(`button`,{type:`button`,onClick:()=>setOn(``),children:`Today`}):null,"
      "(0,L.jsx)(`input`,{type:`date`,className:`vis-cal`,value:on||_ppLD(),max:_ppLD(),min:d.first_day||void 0,onChange:ev=>setOn(ev.target.value===_ppLD()?``:ev.target.value),\"aria-label\":`Pick a day`})]})]})", 'calendar')
patch("rows.length?rows.map(x=>(0,L.jsxs)(`div`,{className:`vis-day`,children:[",
      "rows.length?rows.map(x=>(0,L.jsxs)(`div`,{className:`vis-day`+(by===`day`?` tap`:``)+(by===`day`&&(on||_ppLD())===x.day?` sel`:``),onClick:by===`day`?()=>{setOn(x.day===_ppLD()?``:x.day);try{document.querySelector(`.vis-sec:nth-of-type(2)`)}catch(e){}}:void 0,children:[", 'tap a day')
patch("body .lb-ic{", "body .vis-cal{background:#1a1d27;border:1px solid #2e303a;border-radius:999px;color:#e2e8f0;font:inherit;font-size:12px;font-weight:700;padding:2px 8px;letter-spacing:0;text-transform:none;color-scheme:dark}body .vis-day.tap{cursor:pointer;border-radius:8px;margin:0 -6px;padding:4px 6px}body .vis-day.sel{background:rgba(192,132,252,.12)}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
