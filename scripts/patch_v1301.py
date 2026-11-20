#!/usr/bin/env python3
"""Patch v1300 -> v1301: Share sheet keyboard gap, take 3.
On iPhone Safari the strip above the keyboard (form bar + address pill) shows the page itself, outside the area
fixed elements can draw in, so nothing pinned (sheet, tail, backdrop) can cover it. While the message box has focus,
the page (#root) is hidden and the page background takes the sheet's colour (black in the post scroller), so that
strip matches the sheet. Everything comes back on blur / close."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1300.js'
dst = '_deploy/assets/index-DUcNPOLc-v1301.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("onChange:ev=>setMsg(ev.target.value),onKeyDown:",
      "onChange:ev=>setMsg(ev.target.value),onFocus:()=>document.documentElement.classList.add(`ps-kb`),onBlur:()=>setTimeout(()=>{if(!(document.activeElement&&document.activeElement.closest&&document.activeElement.closest(`.ps-sheet`)&&document.activeElement.tagName===`INPUT`))document.documentElement.classList.remove(`ps-kb`)},50),onKeyDown:", 'focus class')
patch("window._ppShare=id=>{try{if(!id||!localStorage.getItem(`auth_token`))return!1;const host=document.createElement(`div`);document.body.appendChild(host);const r=(0,g.createRoot)(host);",
      "window._ppShare=id=>{try{if(!id||!localStorage.getItem(`auth_token`))return!1;const host=document.createElement(`div`);document.body.appendChild(host);const r=(0,g.createRoot)(host);const _unkb=()=>document.documentElement.classList.remove(`ps-kb`);", 'helper')
patch("r.render((0,L.jsx)(_ShareSheet,{id,close:()=>{setTimeout(()=>{try{r.unmount()}catch(e){}host.remove()},0)}}));",
      "r.render((0,L.jsx)(_ShareSheet,{id,close:()=>{_unkb();setTimeout(()=>{try{r.unmount()}catch(e){}host.remove()},0)}}));", 'clear on close')
patch("body .ps-note{", "html.ps-kb,html.ps-kb body{background:#161920!important}html.ps-kb.reel-shown,html.ps-kb.reel-shown body{background:#000!important}html.ps-kb #root{visibility:hidden}body .ps-note{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
