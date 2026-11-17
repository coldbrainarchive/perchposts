#!/usr/bin/env python3
"""Patch v1144 -> v1145: mod panel → Flock tab gets a "Sign-up limit" switch: Unlimited / 4 a day / 4 a week
(new birds per network). Admins can change it; mods see it read-only. Worker route /site-settings."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1144.js'
dst = '_deploy/assets/index-DUcNPOLc-v1145.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

COMP = r'''function _SignupLimit(){const[st,setSt]=(0,_.useState)(null),[busy,setBusy]=(0,_.useState)(!1),[err,setErr]=(0,_.useState)(``);
 (0,_.useEffect)(()=>{fetch(`${R}/site-settings`,{headers:er()}).then(r=>r.ok?r.json():null).then(d=>d&&setSt(d)).catch(()=>{})},[]);
 if(!st)return null;
 const set=async v=>{if(!st.can_edit||busy||v===st.signup_limit)return;setBusy(!0);setErr(``);try{const r=await fetch(`${R}/site-settings`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({signup_limit:v})});const d=await r.json().catch(()=>({}));if(r.ok)setSt(d);else setErr(d.error||`Could not save`)}catch(e){setErr(`Could not save`)}setBusy(!1)};
 const cap=st.cap||4,opts=[[`off`,`Unlimited`],[`day`,`${cap} a day`],[`week`,`${cap} a week`]];
 const say=st.signup_limit===`day`?`Each network can hatch ${cap} new birds a day.`:st.signup_limit===`week`?`Each network can hatch ${cap} new birds a week.`:`Anyone can hatch as many birds as they like. Good for testing; set a limit before going public.`;
 return(0,L.jsxs)(`div`,{className:`content-card su-lim`,children:[
  (0,L.jsxs)(`div`,{className:`su-top`,children:[(0,L.jsxs)(`div`,{children:[(0,L.jsx)(`div`,{className:`su-t`,children:`Sign-up limit`}),(0,L.jsx)(`div`,{className:`su-s`,children:`New birds per network`})]}),
   (0,L.jsx)(`div`,{className:`su-opts`,children:opts.map(([k,lb])=>(0,L.jsx)(`button`,{type:`button`,disabled:!st.can_edit||busy,className:`mod-tool fs`+(st.signup_limit===k?` on`:``),onClick:()=>set(k),children:lb},k))})]}),
  (0,L.jsx)(`div`,{className:`su-say`,children:st.can_edit?say:say+` Only admins can change this.`}),err?(0,L.jsx)(`div`,{className:`su-err`,children:err}):null]})}
'''
patch("function _PFTabs({u,on}){", COMP + "function _PFTabs({u,on}){", 'component')
patch("_adm&&_tb===`huddles`&&(0,L.jsx)(`div`,{style:{marginTop:16},children:(0,L.jsx)(_HxAdm,{})}),",
      "_tb===`flock`&&(0,L.jsx)(_SignupLimit,{},`sul`),_adm&&_tb===`huddles`&&(0,L.jsx)(`div`,{style:{marginTop:16},children:(0,L.jsx)(_HxAdm,{})}),", 'on the Flock tab')
css = ("body .su-lim{margin-top:16px;padding:14px 18px}body .su-top{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}"
       "body .su-t{color:#f8fafc;font-size:15px;font-weight:700}body .su-s{color:#64748b;font-size:12px;margin-top:2px}"
       "body .su-opts{display:flex;gap:6px;flex-wrap:wrap}body .su-opts .mod-tool:disabled{opacity:.55;cursor:default}body .su-opts .mod-tool.on:disabled{opacity:1}"
       "body .su-say{color:#94a3b8;font-size:12.5px;margin-top:10px;line-height:1.4}body .su-err{color:#f87171;font-size:12.5px;margin-top:6px}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
