#!/usr/bin/env python3
"""Patch v994 -> v995: admin "See all huddles" switch at the top of the mod panel (admins only).
On: the Huddles space shows every huddle and you can open them. Off: only huddles you're in, like everyone else.
Mods no longer see huddles they aren't in (server side)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v994.js'
dst = '_deploy/assets/index-DUcNPOLc-v995.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('gap:16,marginBottom:24},children:null}),(0,L.jsx)(`div`,{className:`mod-tabs`',
      'gap:16,marginBottom:24},children:null}),_adm&&(0,L.jsx)(_HxAdm,{}),(0,L.jsx)(`div`,{className:`mod-tabs`', 'switch in mod panel')
c += r'''
function _HxAdm(){const[on,setOn]=(0,_.useState)(null),[busy,setBusy]=(0,_.useState)(!1);
 (0,_.useEffect)(()=>{fetch(`${R}/admin-huddle-view`,{headers:er()}).then(r=>r.json()).then(d=>setOn(!!d.on)).catch(()=>setOn(!1))},[]);
 const flip=async()=>{if(on===null||busy)return;const nv=!on;setBusy(!0);setOn(nv);
  try{const r=await fetch(`${R}/admin-huddle-view`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({on:nv})});const d=await r.json();setOn(!!d.on)}catch(e){setOn(!nv)}setBusy(!1)};
 return(0,L.jsxs)(`div`,{className:`content-card hxa`,children:[(0,L.jsxs)(`div`,{className:`hxa-t`,children:[(0,L.jsx)(`div`,{className:`hxa-h`,children:`👥 See all huddles`}),
  (0,L.jsx)(`div`,{className:`hxa-d`,children:on?`On: every huddle shows in your Huddles space and you can open any of them.`:`Off: you only see huddles you're in, like everyone else.`})]}),
  (0,L.jsx)(`button`,{type:`button`,role:`switch`,"aria-checked":!!on,"aria-label":`See all huddles`,disabled:on===null,className:`hxa-sw`+(on?` on`:``),onClick:flip,children:(0,L.jsx)(`span`,{})})]})}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.hxa{display:flex;align-items:center;gap:14px;padding:14px 18px;margin:0 0 16px}
.hxa-t{flex:1;min-width:0}
.hxa-h{font-size:15px;font-weight:800;color:#f8fafc}
.hxa-d{margin-top:3px;font-size:12.5px;color:#94a3b8;line-height:1.4}
.hxa-sw{flex-shrink:0;position:relative;width:50px;height:30px;border-radius:999px;border:0;padding:0;background:#374151;cursor:pointer;transition:background .2s}
.hxa-sw span{position:absolute;top:3px;left:3px;width:24px;height:24px;border-radius:999px;background:#f8fafc;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.4)}
.hxa-sw.on{background:#c084fc}.hxa-sw.on span{transform:translateX(20px)}
.hxa-sw:disabled{opacity:.5}
@media (prefers-reduced-motion: reduce){.hxa-sw,.hxa-sw span{transition:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
