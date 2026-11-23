#!/usr/bin/env python3
"""Patch v1335 -> v1336: admins edit all of a post's tags from Mod tools on the post page.
"Tags" button (admins) opens a sheet like the New Post dropdown: current perch tag / region-country / flock tag as
pills at the top (tap to remove), the same search + Tags/Region columns to pick. Changes are a draft: Undo steps back
one change at a time, Save sends them all (worker /post-tags). Works on news bot posts (perch tag + country only).
The old flock-tag pencil/+ next to the pills is gone (this replaces it)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1335.js'
dst = '_deploy/assets/index-DUcNPOLc-v1336.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

# 1) Mod tools: admin "Tags" button before Archive
patch("t===`admin`&&!c.frozen&&(0,L.jsxs)(`button`,{type:`button`,className:`mod-tool`,onClick:async()=>{if(!confirm(`Archive this post?",
      "t===`admin`&&!c.is_huddle&&!/cage/i.test(String(c.community_id||c.board||``))&&(0,L.jsxs)(`button`,{type:`button`,className:`mod-tool`,onClick:()=>window._ppEditTags&&window._ppEditTags(c,cr(c),()=>P()),children:[(0,L.jsx)(`span`,{className:`pp-ic mt-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`HASH`)}}),`Tags`]}),t===`admin`&&!c.frozen&&(0,L.jsxs)(`button`,{type:`button`,className:`mod-tool`,onClick:async()=>{if(!confirm(`Archive this post?", 'mod tools button')

# 2) the old pencil / + flock tag goes (the sheet replaces it); pill refreshes after a save
patch("const canSet=!bot&&!cage&&adm,canRm=!!tag&&adm;", "const canSet=!1,canRm=!1;", 'no pencil')
patch("(0,L.jsx)(_UTagEdit,{post:c},`ute-`+c.id)", "(0,L.jsx)(_UTagEdit,{post:c},`ute-`+c.id+`-`+(c.utag||``))", 'pill key')

# 3) the sheet
patch("body .lb-ic{", "body .pte-back{position:fixed;inset:0;z-index:9650;background:rgba(0,0,0,.55);display:flex;align-items:flex-start;justify-content:center;padding:70px 16px 16px;overflow-y:auto}"
 "body .pte{width:100%;max-width:360px;background:#1e2028;border:1px solid #374151;border-radius:14px;box-shadow:0 12px 40px rgba(0,0,0,.6);display:flex;flex-direction:column;animation:utagPopIn .16s ease-out}"
 "body .pte-top{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding:12px 12px 10px;border-bottom:1px solid #2a2d38;min-height:24px}"
 "body .pte-lb{width:100%;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#64748b;margin-bottom:2px}"
 "body .pte-top>button{background:none;border:0;padding:0;cursor:pointer;display:inline-flex}"
 "body .pte-empty{font-size:12px;color:#64748b;font-weight:600}"
 "body .pte .search-columns{max-height:300px;overflow-y:auto}"
 "body .pte-msg{padding:8px 12px 0;font-size:12px;font-weight:600;color:#f87171}"
 "body .pte-msg.soft{color:#94a3b8}"
 "body .pte-bar{display:flex;align-items:center;gap:8px;padding:10px 12px 12px;border-top:1px solid #2a2d38}"
 "body .pte-bar button{height:32px;border-radius:999px;padding:0 14px;font:inherit;font-size:12px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;cursor:pointer;border:1px solid #374151;background:#14161c;color:#cbd5e1}"
 "body .pte-bar button:disabled{opacity:.4;cursor:default}"
 "body .pte-bar .pte-save{margin-left:auto;background:#a855f7;border-color:#a855f7;color:#fff}"
 "body .lb-ic{", 'css')

c += r"""
function _PostTagEdit({post,boardName,close,saved}){
 const bot=String(post.browser_id||``).startsWith(`bot-`)||/Bot$/.test(post.username||``);
 const bn=post.board_auto?null:(nr.find(e=>e.name===boardName)||nr.find(e=>e.slug===String(post.community_id||post.board||``).toLowerCase())||nr.find(e=>e.name.toLowerCase()===String(post.board||``).toLowerCase()));
 const start={b:bn&&!bn.virtual?bn.slug:``,r:post.continent||``,c:post.country||``,t:post.utag||``};
 const[d,setD]=(0,_.useState)(start),[hist,setHist]=(0,_.useState)([]),[S,setS]=(0,_.useState)(null),[busy,setBusy]=(0,_.useState)(!1),[err,setErr]=(0,_.useState)(``),[pk,setPk]=(0,_.useState)(0),picked=(0,_.useRef)(!1);
 const dRef=(0,_.useRef)(d);dRef.current=d;
 const put=f=>{const cur=dRef.current,nx={...cur,...f(cur)};if(nx.b===cur.b&&nx.r===cur.r&&nx.c===cur.c&&nx.t===cur.t)return;dRef.current=nx;setHist(h=>[...h,cur]);setD(nx);setErr(``)};
 const undo=()=>{if(!hist.length)return;const p=hist[hist.length-1];dRef.current=p;setD(p);setHist(hist.slice(0,-1));setErr(``)};
 const pickBoard=s=>put(()=>({b:s||``}));
 const pickCountry=n=>{picked.current=!0;put(cur=>n?{c:n,r:ar[n]||cur.r}:{c:``});setS(null)};
 const pickRegion=r=>{put(cur=>({r,c:cur.c&&ar[cur.c]!==r?``:cur.c}));setS(r)};
 (0,_.useEffect)(()=>{const on=e=>{picked.current=!0;if(bot){setErr(`News posts can't have a flock tag`);return}const t=String(e.detail||``);put(()=>({t}))};addEventListener(`pp-np-utag`,on);
  const k=e=>{if(e.key===`Escape`&&!document.activeElement?.closest?.(`.np-in`))close()};addEventListener(`keydown`,k);return()=>{removeEventListener(`pp-np-utag`,on);removeEventListener(`keydown`,k)}},[]);
 const pClose=()=>{if(picked.current){picked.current=!1;setPk(n=>n+1);return}close()};
 const same=d.b===start.b&&d.r===start.r&&d.c===start.c&&d.t===start.t;
 const need=bot?(!d.b?`News posts need a perch tag`:``):(!d.b&&!d.t?`A post needs at least one tag`:``);
 const save=async()=>{if(same||need||busy)return;setBusy(!0);setErr(``);const b=d.b?nr.find(e=>e.slug===d.b):null;
  try{const r=await fetch(`${R}/post-tags`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({post_id:post.id,board:b?{slug:b.slug,name:b.name}:null,continent:d.c?(ar[d.c]||d.r||null):(d.r||null),country:d.c||null,tag:d.t||``})});const j=await r.json().catch(()=>({}));
   if(r.ok){saved&&saved(j);close();return}setErr(j.error||`Couldn't save the tags`)}catch(e){setErr(`Couldn't save the tags`)}setBusy(!1)};
 const boards=nr.filter(e=>!e.virtual&&![`feedback`,`cage`].includes(e.slug));
 const bObj=d.b?nr.find(e=>e.slug===d.b):null;
 const rmBtn=(k,kids,f)=>(0,L.jsx)(`button`,{type:`button`,"aria-label":`Remove`,onClick:ev=>{const el=ev.currentTarget;el.classList.add(`np-out`);setTimeout(()=>{el.classList.remove(`np-out`);put(f)},170)},children:kids},k);
 const pills=[bObj?rmBtn(`b`,(0,L.jsx)(Ar,{boardName:bObj.name,small:!0}),()=>({b:``})):null,
  d.c?rmBtn(`c`,(0,L.jsx)(kr,{country:d.c,small:!0}),()=>({c:``})):d.r?rmBtn(`r`,(0,L.jsx)(kr,{continent:d.r,small:!0}),()=>({r:``})):null,
  d.t?rmBtn(`t`,(0,L.jsx)(_UTag,{tag:d.t,small:!0}),()=>({t:``})):null].filter(Boolean);
 const ring=on=>({outline:`none`,boxShadow:on?`0 0 0 2px #c084fc`:`none`,borderRadius:999,alignSelf:`flex-start`,justifyContent:`flex-start`});
 const cols=(0,L.jsxs)(`div`,{className:`search-columns`,children:[(0,L.jsxs)(`div`,{className:`search-column`,style:{alignContent:`flex-start`},children:[(0,L.jsx)(`div`,{className:`search-section-label`,children:`Perch tags`}),
   boards.map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>pickBoard(e.slug===d.b?``:e.slug),style:ring(e.slug===d.b),children:(0,L.jsx)(Ar,{boardName:e.name,small:!0})},e.slug))]}),
  (0,L.jsx)(`div`,{className:`search-column`,children:S?(0,L.jsxs)(L.Fragment,{children:[(0,L.jsxs)(`div`,{className:`search-section-label`,style:{display:`flex`,alignItems:`center`,gap:4},children:[(0,L.jsx)(`button`,{type:`button`,onClick:()=>setS(null),style:{background:`none`,border:`none`,color:`#c084fc`,fontSize:11,fontWeight:700,cursor:`pointer`,padding:0},children:`← Back`}),(0,L.jsx)(`span`,{children:S})]}),
    (0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`,width:`100%`,gap:4},children:or.filter(e=>ar[e.name]===S).map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>{put(cur=>e.name===cur.c?{c:``}:{c:e.name,r:ar[e.name]||cur.r});setS(null)},style:ring(e.name===d.c),children:(0,L.jsx)(kr,{country:e.name,small:!0})},e.name))})]})
   :(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`div`,{className:`search-section-label`,children:`Region`}),(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`,width:`100%`,gap:4},children:rr.filter(e=>e!==`World`).map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>pickRegion(e),style:ring(d.c?ar[d.c]===e:d.r===e),children:(0,L.jsx)(kr,{continent:e,small:!0})},e))})]})})]});
 return(0,L.jsx)(`div`,{className:`pte-back`,onClick:e=>{if(e.target===e.currentTarget)close()},children:(0,L.jsxs)(`div`,{className:`pte`,role:`dialog`,"aria-label":`Edit tags`,children:[
  (0,L.jsxs)(`div`,{className:`pte-top`,children:[(0,L.jsx)(`div`,{className:`pte-lb`,children:bot?`Edit tags · news post`:`Edit tags`}),...(pills.length?pills:[(0,L.jsx)(`span`,{className:`pte-empty`,children:`No tags`},`e`)])]}),
  (0,L.jsx)(_NpPicker,{close:pClose,pickBoard,pickCountry,pickRegion,cur:d.b,curC:d.c,curR:d.r,caged:!1,cols},`np`+pk),
  err||need?(0,L.jsx)(`div`,{className:`pte-msg`+(err?``:` soft`),children:err||need}):null,
  (0,L.jsxs)(`div`,{className:`pte-bar`,children:[(0,L.jsx)(`button`,{type:`button`,onClick:undo,disabled:!hist.length||busy,children:`Undo`}),(0,L.jsx)(`button`,{type:`button`,onClick:close,disabled:busy,children:`Cancel`}),(0,L.jsx)(`button`,{type:`button`,className:`pte-save`,onClick:save,disabled:same||!!need||busy,children:busy?`Saving…`:`Save`})]})]})})}
window._ppEditTags=(post,boardName,saved)=>{try{const host=document.createElement(`div`);document.body.appendChild(host);const r=(0,g.createRoot)(host);
 r.render((0,L.jsx)(_PostTagEdit,{post,boardName,saved,close:()=>setTimeout(()=>{try{r.unmount()}catch(e){}host.remove()},0)}))}catch(e){console.error(e)}};
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
