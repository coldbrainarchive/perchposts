#!/usr/bin/env python3
"""Patch v1275 -> v1276: Visitors tab keeps all-time history: a 14 days / Months / Years switch.
Months = last 12 months, Years = every year; each shows unique members and guests in that period."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1275.js'
dst = '_deploy/assets/index-DUcNPOLc-v1276.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("[err,setErr]=(0,_.useState)(``);\n (0,_.useEffect)(()=>{let dead=!1;const load=()=>fetch(`${R}/visitors?d=${_ppLD()}${hide?`&hide_me=1`:``}`",
      "[err,setErr]=(0,_.useState)(``),[by,setBy]=(0,_.useState)(`day`);\n (0,_.useEffect)(()=>{let dead=!1;const load=()=>fetch(`${R}/visitors?d=${_ppLD()}${hide?`&hide_me=1`:``}${by!==`day`?`&by=${by}`:``}`", 'by state + fetch')
patch("return()=>{dead=!0;clearInterval(t)}},[hide]);", "return()=>{dead=!0;clearInterval(t)}},[hide,by]);", 'refetch on by')
patch("const mx=d?Math.max(1,...d.days.map(x=>(x.members||0)+(x.guests||0))):1;",
      "const rows=d?(by!==`day`&&d.by===by&&d.periods?d.periods:d.days):[];const mx=Math.max(1,...rows.map(x=>(x.members||0)+(x.guests||0)));"
      "const lab=s=>by===`year`?s:by===`month`?(()=>{try{const[y,m]=s.split(`-`).map(Number);return new Date(y,m-1,1).toLocaleDateString(void 0,{month:`short`,year:`numeric`})}catch(e){return s}})():fd(s);", 'rows by period')
patch("(0,L.jsx)(`div`,{className:`vis-h`,children:`Last 14 days`}),d.days.length?d.days.map(x=>(0,L.jsxs)(`div`,{className:`vis-day`,children:[(0,L.jsx)(`span`,{className:`vis-dl`,children:fd(x.day)})",
      "(0,L.jsxs)(`div`,{className:`vis-h vis-hs`,children:[by===`day`?`Last 14 days`:by===`month`?`Last 12 months`:`By year`,(0,L.jsx)(`span`,{className:`vis-by`,children:[[`day`,`14 days`],[`month`,`Months`],[`year`,`Years`]].map(([k,lb])=>(0,L.jsx)(`button`,{type:`button`,className:by===k?`on`:``,onClick:()=>setBy(k),children:lb},k))})]}),rows.length?rows.map(x=>(0,L.jsxs)(`div`,{className:`vis-day`,children:[(0,L.jsx)(`span`,{className:`vis-dl`,children:lab(x.day)})", 'switch + labels')
patch("`A visitor is one phone or computer with the site open. Online = seen in the last 3 minutes.",
      "`A visitor is one phone or computer with the site open. Months and years count each visitor once per period; history is kept forever. Online = seen in the last 3 minutes.", 'note')
patch("body .lb-ic{", "body .vis-hs{justify-content:space-between}body .vis-by{display:flex;gap:4px}body .vis-by button{padding:3px 9px;border-radius:999px;border:1px solid #2e303a;background:none;color:#94a3b8;font:inherit;font-size:11px;letter-spacing:0;text-transform:none;font-weight:700;cursor:pointer}body .vis-by button.on{background:#c084fc;border-color:#c084fc;color:#14081d}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
