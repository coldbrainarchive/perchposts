#!/usr/bin/env python3
"""Patch v1184 -> v1186 (v1185 was rolled back): the profile's Posts / Flaps buttons become a small sliding
toggle like the chat's Oldest / Newest one (same purple thumb slide), centred; no flaps icon."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1184.js'
dst = '_deploy/assets/index-DUcNPOLc-v1186.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("""function _PFTabs({u,on}){const q=encodeURIComponent(u);return(0,L.jsxs)(`div`,{className:`pf-tabs`,children:[
 (0,L.jsx)(I,{to:`/?user=${q}`,replace:!0,className:`pf-tab`+(on?``:` on`),children:`Posts`}),
 (0,L.jsxs)(I,{to:`/?user=${q}&flaps=1`,replace:!0,className:`pf-tab`+(on?` on`:``),children:[(0,L.jsx)(`span`,{className:`pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),`Flaps`]})]})}""",
"""function _PFTabs({u,on}){const q=encodeURIComponent(u),nav=nt();return(0,L.jsx)(`div`,{className:`pf-tabs pf-slide`,children:(0,L.jsxs)(`div`,{className:`sort-toggle pf-toggle`,role:`tablist`,children:[
 (0,L.jsx)(`button`,{type:`button`,role:`tab`,"aria-selected":!on,className:`sort-toggle-btn pf-tab`+(on?``:` active on`),onClick:()=>{if(on)nav(`/?user=${q}`,{replace:!0})},children:`Posts`}),
 (0,L.jsx)(`button`,{type:`button`,role:`tab`,"aria-selected":!!on,className:`sort-toggle-btn pf-tab`+(on?` active on`:``),onClick:()=>{if(!on)nav(`/?user=${q}&flaps=1`,{replace:!0})},children:`Flaps`})]})})}""", 'slider toggle')
patch("body .lb-ic{",
      "body .pf-tabs.pf-slide{display:flex!important;justify-content:center;gap:0!important;padding:0!important;background:none!important;border:0!important}"
      "body .pf-toggle .sort-toggle-btn.pf-tab{flex:none!important;height:28px!important;min-height:0!important;padding:0 18px!important;font-size:13px!important;border:0!important;border-radius:999px!important;box-shadow:none!important;background:transparent;color:#c084fc;position:relative;z-index:1}"
      "body .pf-toggle .sort-toggle-btn.pf-tab.active{color:#fff;background:transparent}"
      "body .pf-toggle:not(.tg-ready) .sort-toggle-btn.pf-tab.active{background:#c084fc}"
      "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
