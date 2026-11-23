#!/usr/bin/env python3
"""Patch v1314 -> v1315: mod panel Settings (admins): "Blocked tags" card — block a word (it's removed from every post
and can't be used again) or unblock it. Uses /blocked-tags."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1314.js'
dst = '_deploy/assets/index-DUcNPOLc-v1315.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("(0,L.jsx)(_SignupLimit,{},`sul`),(0,L.jsx)(_AiCheck,{},`aic`),", "(0,L.jsx)(_SignupLimit,{},`sul`),(0,L.jsx)(_AiCheck,{},`aic`),(0,L.jsx)(_BlockedTags,{},`btg`),", 'settings card')
patch("body .lb-ic{", "body .btg-row{display:flex;gap:8px;margin-top:10px}body .btg-row input{flex:1;min-width:0;height:36px;border-radius:999px;border:1px solid #2e303a;background:#0d0f14;color:#e2e8f0;padding:0 14px;font:inherit;font-size:16px}body .btg-list{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}body .btg-it{display:inline-flex;align-items:center;gap:6px}body .btg-it button{border:0;background:none;color:#fca5a5;font:inherit;font-size:12px;font-weight:700;cursor:pointer;padding:0 2px}body .lb-ic{", 'css')
c += r"""
function _BlockedTags(){const[list,setList]=(0,_.useState)(null),[v,setV]=(0,_.useState)(``),[err,setErr]=(0,_.useState)(``),[busy,setBusy]=(0,_.useState)(!1);
 const call=async body=>{setBusy(!0);setErr(``);try{const r=await fetch(`${R}/blocked-tags`,body?{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify(body)}:{headers:er()});const d=await r.json().catch(()=>({}));if(r.ok)setList(d.blocked||[]);else setErr(d.error||`Couldn't save`)}catch(e){setErr(`Couldn't save`)}setBusy(!1)};
 (0,_.useEffect)(()=>{call(null)},[]);
 const t=v.replace(/^#+/,``).replace(/[^A-Za-z0-9]/g,``).toLowerCase().slice(0,20);
 const block=()=>{if(!/^[a-z0-9]{2,20}$/.test(t)||busy)return;if(!confirm(`Block #${t}? It's removed from every post and nobody can use it.`))return;call({tag:t}).then(()=>setV(``))};
 return(0,L.jsxs)(`div`,{className:`content-card su-lim`,children:[(0,L.jsxs)(`div`,{className:`su-top`,children:[(0,L.jsxs)(`div`,{children:[(0,L.jsx)(`div`,{className:`su-t`,children:`Blocked tags`}),(0,L.jsx)(`div`,{className:`su-s`,children:`Words nobody can use as a #tag`})]})]}),
  (0,L.jsxs)(`div`,{className:`btg-row`,children:[(0,L.jsx)(`input`,{type:`search`,name:`search_btg`,autoComplete:`off`,autoCapitalize:`off`,placeholder:`#word`,value:v,onChange:e=>setV(e.target.value),onKeyDown:e=>{if(e.key===`Enter`){e.preventDefault();block()}}}),(0,L.jsx)(`button`,{type:`button`,className:`mod-tool fs danger`,disabled:busy||!/^[a-z0-9]{2,20}$/.test(t),onClick:block,children:`Block`})]}),
  list&&list.length?(0,L.jsx)(`div`,{className:`btg-list`,children:list.map(x=>(0,L.jsxs)(`span`,{className:`btg-it`,children:[(0,L.jsx)(_UTag,{tag:x.tag,small:!0}),(0,L.jsx)(`button`,{type:`button`,disabled:busy,onClick:()=>call({tag:x.tag,block:!1}),children:`Unblock`})]},x.tag))}):list?(0,L.jsx)(`div`,{className:`su-say`,children:`No blocked tags. Swearing and slurs are already refused automatically.`}):null,
  err?(0,L.jsx)(`div`,{className:`su-err`,children:err}):null]})}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
