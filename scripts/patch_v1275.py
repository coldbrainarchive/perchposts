#!/usr/bin/env python3
"""Patch v1274 -> v1275: visitor counter.
- Every open, visible page pings /ping every 2 minutes (and when it comes back into view) with the device's browser id
  and local date. Hidden tabs don't ping.
- Mod panel: admins get a Visitors tab: online now (members by name + guest count), today, last 14 days, with a
  "Hide me" switch (remembered on this device, on by default)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1274.js'
dst = '_deploy/assets/index-DUcNPOLc-v1275.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("..._adm?[[`bot`,`Bot`,null],[`settings`,`Settings`,null]]:[]]",
      "..._adm?[[`visitors`,`Visitors`,null],[`bot`,`Bot`,null],[`settings`,`Settings`,null]]:[]]", 'Visitors tab (admins)')
patch("_tb===`flagged`&&(0,L.jsx)(_AiFlags,{},`aif`),",
      "_tb===`flagged`&&(0,L.jsx)(_AiFlags,{},`aif`),_adm&&_tb===`visitors`&&(0,L.jsx)(_Visitors,{},`vis`),", 'Visitors body')
VIS = r"""function _ppLD(t){t=t||new Date();return t.getFullYear()+`-`+String(t.getMonth()+1).padStart(2,`0`)+`-`+String(t.getDate()).padStart(2,`0`)}
function _Visitors(){const[d,setD]=(0,_.useState)(null),[hide,setHide]=(0,_.useState)(()=>{try{return localStorage.getItem(`visHideMe`)!==`0`}catch(e){return!0}}),[err,setErr]=(0,_.useState)(``);
 (0,_.useEffect)(()=>{let dead=!1;const load=()=>fetch(`${R}/visitors?d=${_ppLD()}${hide?`&hide_me=1`:``}`,{headers:er()}).then(r=>r.ok?r.json():Promise.reject()).then(x=>{if(!dead){setD(x);setErr(``)}}).catch(()=>{if(!dead)setErr(`Couldn't load visitors`)});load();const t=setInterval(()=>{document.visibilityState===`visible`&&load()},30000);return()=>{dead=!0;clearInterval(t)}},[hide]);
 const pick=v=>{setHide(v);try{localStorage.setItem(`visHideMe`,v?`1`:`0`)}catch(e){}};
 const nm=a=>a.length?(0,L.jsx)(`div`,{className:`vis-names`,children:a.map(n=>(0,L.jsx)(`span`,{className:`vis-name`,children:n},n))}):null;
 const big=(n,lb)=>(0,L.jsxs)(`div`,{className:`vis-big`,children:[(0,L.jsx)(`b`,{children:n}),(0,L.jsx)(`span`,{children:lb})]});
 const fd=s=>{try{const[y,m,dd]=s.split(`-`).map(Number);return new Date(y,m-1,dd).toLocaleDateString(void 0,{weekday:`short`,month:`short`,day:`numeric`})}catch(e){return s}};
 const mx=d?Math.max(1,...d.days.map(x=>(x.members||0)+(x.guests||0))):1;
 return(0,L.jsxs)(`div`,{className:`set-tab`,children:[(0,L.jsxs)(`div`,{className:`content-card su-lim`,children:[
  (0,L.jsxs)(`div`,{className:`su-top`,children:[(0,L.jsxs)(`div`,{children:[(0,L.jsx)(`div`,{className:`su-t`,children:`Visitors`}),(0,L.jsx)(`div`,{className:`su-s`,children:`Members are signed in · guests aren't`})]}),
   (0,L.jsx)(`div`,{className:`su-opts`,children:[[!0,`Hide me`],[!1,`Show me`]].map(([k,lb])=>(0,L.jsx)(`button`,{type:`button`,className:`mod-tool fs`+(hide===k?` on`:``),onClick:()=>pick(k),children:lb},lb))})]}),
  err?(0,L.jsx)(`div`,{className:`su-err`,children:err}):null,
  d?(0,L.jsxs)(L.Fragment,{children:[
   (0,L.jsxs)(`div`,{className:`vis-sec`,children:[(0,L.jsxs)(`div`,{className:`vis-h`,children:[(0,L.jsx)(`span`,{className:`vis-dot`}),`Online now`]}),(0,L.jsxs)(`div`,{className:`vis-row`,children:[big(d.online.members.length,`members`),big(d.online.guests,`guests`)]}),nm(d.online.members)]}),
   (0,L.jsxs)(`div`,{className:`vis-sec`,children:[(0,L.jsx)(`div`,{className:`vis-h`,children:`Today`}),(0,L.jsxs)(`div`,{className:`vis-row`,children:[big(d.today.members.length,`members`),big(d.today.guests,`guests`)]}),nm(d.today.members)]}),
   (0,L.jsxs)(`div`,{className:`vis-sec`,children:[(0,L.jsx)(`div`,{className:`vis-h`,children:`Last 14 days`}),d.days.length?d.days.map(x=>(0,L.jsxs)(`div`,{className:`vis-day`,children:[(0,L.jsx)(`span`,{className:`vis-dl`,children:fd(x.day)}),(0,L.jsxs)(`span`,{className:`vis-bar`,children:[(0,L.jsx)(`i`,{className:`m`,style:{width:(x.members||0)/mx*100+`%`}}),(0,L.jsx)(`i`,{className:`g`,style:{width:(x.guests||0)/mx*100+`%`}})]}),(0,L.jsx)(`span`,{className:`vis-dn`,children:`${x.members||0} · ${x.guests||0}`})]},x.day)):(0,L.jsx)(`div`,{className:`su-say`,children:`No visits yet.`}),(0,L.jsxs)(`div`,{className:`vis-key`,children:[(0,L.jsx)(`i`,{className:`m`}),`members`,(0,L.jsx)(`i`,{className:`g`}),`guests`]})]}),
   (0,L.jsx)(`div`,{className:`su-say`,children:`A visitor is one phone or computer with the site open. Online = seen in the last 3 minutes. Hide me also leaves out your devices while signed out. Updates every 30 s.`})]}):null]})]})}
function _AiFlags("""
patch("function _AiFlags(", VIS, 'Visitors component')
css = ("body .vis-sec{margin-top:16px}body .vis-h{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:#94a3b8;margin-bottom:8px}"
       "body .vis-dot{width:8px;height:8px;border-radius:50%;background:#4ade80;box-shadow:0 0 6px #4ade80}"
       "body .vis-row{display:flex;gap:10px}body .vis-big{flex:1;display:flex;align-items:baseline;gap:6px;padding:10px 14px;border-radius:12px;background:#1a1d27;border:1px solid rgba(148,163,184,.15)}"
       "body .vis-big b{font-size:24px;color:#f1f5f9}body .vis-big span{font-size:13px;color:#94a3b8}"
       "body .vis-names{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}body .vis-name{padding:3px 9px;border-radius:999px;background:#2a2340;color:#e9d5ff;font-size:12px;font-weight:700}"
       "body .vis-day{display:flex;align-items:center;gap:10px;padding:4px 0;font-size:13px}body .vis-dl{width:96px;flex-shrink:0;color:#cbd5e1}"
       "body .vis-bar{flex:1;display:flex;height:10px;border-radius:5px;background:#1a1d27;overflow:hidden}body .vis-bar i,body .vis-key i{display:block;height:100%}"
       "body .vis-bar .m,body .vis-key .m{background:#c084fc}body .vis-bar .g,body .vis-key .g{background:#475569}"
       "body .vis-dn{width:56px;flex-shrink:0;text-align:right;color:#94a3b8;font-variant-numeric:tabular-nums}"
       "body .vis-key{display:flex;align-items:center;gap:6px;margin-top:8px;font-size:12px;color:#94a3b8}body .vis-key i{width:10px;height:10px;border-radius:3px;margin-left:6px}")
patch("body .lb-ic{", css + "body .lb-ic{", 'css')
c += r"""
;(()=>{try{let last=0;const ping=()=>{try{if(document.visibilityState!==`visible`)return;const n=Date.now();if(n-last<100000)return;last=n;
  let vid=localStorage.getItem(`browser_id`);if(!vid){vid=crypto.randomUUID();localStorage.setItem(`browser_id`,vid)}const tk=localStorage.getItem(`auth_token`);
  fetch(`${R}/ping`,{method:`POST`,headers:{"Content-Type":`application/json`,...(tk?{Authorization:`Bearer ${tk}`}:{})},body:JSON.stringify({vid,d:(t=>t.getFullYear()+`-`+String(t.getMonth()+1).padStart(2,`0`)+`-`+String(t.getDate()).padStart(2,`0`))(new Date())}),keepalive:!0}).catch(()=>{})}catch(e){}};
  setTimeout(ping,1500);setInterval(ping,120000);document.addEventListener(`visibilitychange`,ping)}catch(e){}})();
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
