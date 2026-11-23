#!/usr/bin/env python3
"""Patch v1316 -> v1317: the New Post "Select tag & country" dropdown title is a search box.
Empty: the usual Tags / Region lists. Typing: matching spaces, regions, countries (usa/uk/uae too) and user #tags
(from /tags?q=, plus "Use #word" for a new valid tag). Picking a space/country sets it, a region opens its countries,
a #tag fills the "+ TAG" chip (event pp-np-utag)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1316.js'
dst = '_deploy/assets/index-DUcNPOLc-v1317.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
HEAD_START = "children:[(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,padding:`8px 10px 4px`,borderBottom:`1px solid #2a2d38`}"
HEAD_END = "children:`Select tag & country`})]}),"
i = c.index(HEAD_START); j = c.index(HEAD_END, i) + len(HEAD_END)
assert c.count(HEAD_START) == 1
k = j  # columns element starts here
assert c.startswith("(0,L.jsxs)(`div`,{className:`search-columns`", k)
# find the end of the columns element by bracket matching (skip template literals)
depth = 0; pos = k + len('(0,L.jsxs)'); inbt = False
while True:
    ch = c[pos]
    if inbt:
        if ch == '`': inbt = False
    elif ch == '`': inbt = True
    elif ch in '([{': depth += 1
    elif ch in ')]}':
        depth -= 1
        if depth == 0: pos += 1; break
    pos += 1
cols = c[k:pos]
print('columns end ->', c[pos:pos+12])
assert c[pos:pos+2] == ']}', c[pos:pos+10]
c = c[:i] + "children:(0,L.jsx)(_NpPicker,{close:()=>x(!1),pickBoard:g,pickCountry:e=>{y(e);C(null)},pickRegion:e=>C(e),cur:h,curC:v,caged:p,cols:" + cols + "})" + c[pos+1:]
print('OK: header -> search picker (columns kept as the empty-search view)')
# _UTagPick listens for a tag picked in the dropdown
patch("function _UTagPick(){const[tag,setTag]=(0,_.useState)(``),[ed,setEd]=(0,_.useState)(!1);(0,_.useEffect)(()=>{window._ppNewTag=null;return()=>{window._ppNewTag=null}},[]);",
      "function _UTagPick(){const[tag,setTag]=(0,_.useState)(``),[ed,setEd]=(0,_.useState)(!1);(0,_.useEffect)(()=>{window._ppNewTag=null;const on=ev=>{const t=ev.detail;if(t){setTag(t);window._ppNewTag=t;setEd(!1)}};addEventListener(`pp-np-utag`,on);return()=>{window._ppNewTag=null;removeEventListener(`pp-np-utag`,on)}},[]);", 'tag chip listens')
patch("body .lb-ic{", "body .np-sb{display:flex;align-items:center;gap:8px;padding:8px 10px;border-bottom:1px solid #2a2d38}body .np-sb .np-in{flex:1;display:flex;align-items:center;gap:7px;height:34px;border-radius:999px;background:#14161c;border:1px solid #2e303a;padding:0 12px}body .np-sb .np-in:focus-within{border-color:#c084fc}body .np-sb .np-in .ri{width:15px;height:15px;color:#64748b;flex-shrink:0}body .np-sb input{flex:1;min-width:0;border:0;background:none;outline:none;color:#e2e8f0;font:inherit;font-size:16px}body .np-sb input::-webkit-search-cancel-button{display:none}body .np-res{max-height:320px;overflow-y:auto;padding:4px 0 8px}body .np-res .search-section-label{padding:8px 12px 4px;margin:0}body .np-res .np-row{display:flex;flex-wrap:wrap;gap:6px;padding:2px 12px 6px}body .np-none{padding:14px;color:#64748b;font-size:13px;text-align:center}body .np-new{display:inline-flex;align-items:center;gap:6px;background:none;border:0;padding:0;cursor:pointer;color:#94a3b8;font:inherit;font-size:12px;font-weight:700}body .lb-ic{", 'css')
c += r"""
function _NpPicker({close,pickBoard,pickCountry,pickRegion,cur,curC,caged,cols}){const[q,setQ]=(0,_.useState)(``),[ut,setUt]=(0,_.useState)([]),inp=(0,_.useRef)(null);
 const k=q.trim().toLowerCase(),tk=k.replace(/^#+/,``).replace(/[^a-z0-9]/g,``);
 (0,_.useEffect)(()=>{if(!tk){setUt([]);return}let dead=!1;const t=setTimeout(()=>{fetch(`${R}/tags?q=${encodeURIComponent(tk)}`).then(r=>r.ok?r.json():{tags:[]}).then(d=>{dead||setUt(d.tags||[])}).catch(()=>{})},150);return()=>{dead=!0;clearTimeout(t)}},[tk]);
 const role=Qn()?.role,boards=nr.filter(e=>!e.virtual&&e.slug!==`feedback`&&(e.slug!==`announcements`||[`mod`,`admin`].includes(role))&&(e.slug!==`cage`||[`mod`,`admin`].includes(role)||localStorage.getItem(`_caged`)===`1`));
 const AL={usa:`United States`,us:`United States`,america:`United States`,uk:`United Kingdom`,britain:`United Kingdom`,england:`United Kingdom`,uae:`United Arab Emirates`};
 const kk=k.replace(/^#+/,``);
 const bm=kk&&!caged?boards.filter(e=>e.name.toLowerCase().includes(kk)||e.slug.includes(kk)):[];
 const rm=kk&&!caged?rr.filter(e=>e!==`World`&&e.toLowerCase().includes(kk)):[];
 const cm=kk&&!caged?or.filter(e=>e.name.toLowerCase().includes(kk)||AL[kk]===e.name).slice(0,12):[];
 const canNew=!caged&&/^[a-z0-9]{2,20}$/.test(tk)&&!ut.some(x=>x.tag===tk)&&(k.startsWith(`#`)||!(bm.length||rm.length||cm.length));
 const useTag=t=>{dispatchEvent(new CustomEvent(`pp-np-utag`,{detail:t}));close()};
 const sec=(lb,kids)=>kids&&kids.length?[(0,L.jsx)(`div`,{className:`search-section-label`,children:lb},lb+`l`),(0,L.jsx)(`div`,{className:`np-row`,children:kids},lb+`r`)]:[];
 const hasAny=bm.length||rm.length||cm.length||ut.length||canNew;
 return(0,L.jsxs)(L.Fragment,{children:[(0,L.jsxs)(`div`,{className:`np-sb`,children:[(0,L.jsx)(`button`,{type:`button`,onClick:close,"aria-label":`Close`,style:{display:`flex`,alignItems:`center`,justifyContent:`center`,width:22,height:22,borderRadius:999,border:`none`,background:`#2d2f3a`,color:`#94a3b8`,fontSize:14,lineHeight:1,cursor:`pointer`,padding:0,flexShrink:0},children:`×`}),
   (0,L.jsxs)(`label`,{className:`np-in`,children:[(0,L.jsx)(`span`,{style:{display:`inline-flex`},dangerouslySetInnerHTML:{__html:_ppIco(`SEARCH`)}}),(0,L.jsx)(`input`,{ref:inp,type:`search`,name:`search_np_pick`,autoComplete:`off`,autoCorrect:`off`,autoCapitalize:`off`,spellCheck:!1,placeholder:`Search tags, regions, #tags`,value:q,onChange:e=>setQ(e.target.value),onKeyDown:e=>{if(e.key===`Escape`){e.preventDefault();q?setQ(``):close()}}})]})]}),
  !k?cols:(0,L.jsx)(`div`,{className:`np-res`,children:hasAny?[
   ...sec(`Tags`,bm.map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>{pickBoard(e.slug);setQ(``)},style:{outline:`none`,boxShadow:e.slug===cur?`0 0 0 2px #c084fc`:`none`,borderRadius:999},children:(0,L.jsx)(Ar,{boardName:e.name,small:!0})},e.slug))),
   ...sec(`Regions`,rm.map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>{pickRegion(e);setQ(``)},style:{outline:`none`,borderRadius:999},children:(0,L.jsx)(kr,{continent:e,small:!0})},e))),
   ...sec(`Countries`,cm.map(e=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>{pickCountry(e.name);setQ(``)},style:{outline:`none`,boxShadow:e.name===curC?`0 0 0 2px #c084fc`:`none`,borderRadius:999},children:(0,L.jsx)(kr,{country:e.name,small:!0})},e.name))),
   ...sec(`User tags`,[...ut.map(x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>useTag(x.tag),style:{outline:`none`,borderRadius:999},children:(0,L.jsx)(_UTag,{tag:x.tag,small:!0})},x.tag)),canNew?(0,L.jsxs)(`button`,{type:`button`,className:`np-new`,onClick:()=>useTag(tk),children:[`Use`,(0,L.jsx)(_UTag,{tag:tk,small:!0})]},`new`):null].filter(Boolean))
  ]:(0,L.jsx)(`div`,{className:`np-none`,children:caged?`You can only post in The Cage`:`Nothing matches “${q.trim()}”`})})]})}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
