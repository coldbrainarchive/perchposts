#!/usr/bin/env python3
"""Patch v1338 -> v1339: saved searches (signed-in birds, up to 5, kept on the account via /saved-searches).
- Bookmark button at the end of the search bar when it has filters or keywords: tap to save (filled = saved; tap again
  to remove). Saves flock/board/region/country/flock tag/bird/bots/keywords (not time or sort).
- "Saved" row at the top of the Tags tab: one tap fills the bar. Edit: star one as the default, or remove.
- Default: fills the bar when you open the home page with no filters (once per visit: again after 30 min away)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1338.js'
dst = '_deploy/assets/index-DUcNPOLc-v1339.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch("if(c.current)c.current.value=``};let j=nr.find(e=>e.slug===d),M=",
      "if(c.current)c.current.value=``},_goSaved=qs=>{if(location.pathname!==`/`){location.assign(`/?`+qs);return}clearTimeout(c.current?._dbt);const n=new URLSearchParams(qs);t(n);a(!1);s(null);const q=n.get(`q`)||``;r(q);if(c.current){c.current.value=q;c.current.blur()}},_ssD=(0,_.useEffect)(()=>{_ssDefault(e,_goSaved)},[]);let j=nr.find(e=>e.slug===d),M=", 'go + default')
patch("_tab===`boards`&&(0,L.jsxs)(`div`,{className:`search-column srch-body`,children:[...g.filter(",
      "_tab===`boards`&&(0,L.jsxs)(`div`,{className:`search-column srch-body`,children:[(0,L.jsx)(_SavedSearches,{go:_goSaved},`ssv`),...g.filter(", 'tags tab row')
patch("spellCheck:!1}),]}),E&&(0,L.jsxs)(`div`,{className:`search-dropdown`",
      "spellCheck:!1}),(0,L.jsx)(_SaveSearchBtn,{params:e,kw:n},`ssb`)]}),E&&(0,L.jsxs)(`div`,{className:`search-dropdown`", 'bar button')

patch("body .lb-ic{",
 "body .search-bar:has(>.ss-btn){position:relative;padding-right:40px!important}body .ss-btn{position:absolute;right:8px;top:50%;transform:translateY(-50%);display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;margin:0;border:0;background:none;padding:0;color:#64748b;cursor:pointer;border-radius:999px}"
 "body .ss-btn svg{width:18px;height:18px}body .ss-btn.on{color:#c084fc}body .ss-btn.pop svg{animation:ssPop .32s ease-out}"
 "@keyframes ssPop{0%{transform:scale(1)}45%{transform:scale(1.3)}100%{transform:scale(1)}}"
 "body .ss-wrap{flex-basis:100%;width:100%;margin-bottom:6px;padding-bottom:10px;border-bottom:1px solid #2a2d38;text-align:left}body .ss-hd .search-section-label{flex:1;width:auto;text-align:left!important;padding-left:2px!important;margin:0!important}"
 "body .ss-hd{display:flex;align-items:center;justify-content:space-between}"
 "body .ss-hd .search-section-label{margin:0}"
 "body .ss-ed{background:none;border:0;padding:4px 2px;color:#c084fc;font:inherit;font-size:11px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;cursor:pointer}"
 "body .ss-list{display:flex;flex-direction:column;gap:6px;margin-top:6px}"
 "body .ss-it{display:flex;align-items:center;gap:6px}"
 "body .ss-go{display:flex;flex-wrap:wrap;align-items:center;gap:5px;flex:1;min-width:0;background:#14161c;border:1px solid #2e303a;border-radius:14px;padding:6px 8px;cursor:pointer;text-align:left;font:inherit}"
 "body .ss-go:active{border-color:#c084fc}"
 "body .ss-star{flex-shrink:0;display:inline-flex;width:26px;height:26px;align-items:center;justify-content:center;border:0;background:none;padding:0;color:#475569;cursor:pointer}"
 "body .ss-star svg,body .ss-x svg,body .ss-defic svg{width:16px;height:16px}body .ss-star.on,body .ss-defic{color:#fbbf24}"
 "body .ss-defic{display:inline-flex;margin-right:1px}"
 "body .ss-x{flex-shrink:0;display:inline-flex;width:26px;height:26px;align-items:center;justify-content:center;border:0;background:none;padding:0;color:#f87171;cursor:pointer}"
 "body .ss-kw{display:inline-flex;align-items:center;height:20px;padding:0 8px;border-radius:999px;border:1px solid #475569;color:#cbd5e1;font-size:11px;font-weight:700;white-space:nowrap}"
 "body .ss-none{font-size:12px;line-height:1.45;color:#64748b;margin-top:6px;padding-left:2px;text-align:left}"
 "body .lb-ic{", 'css')

c += r"""
const _SS_KEYS=[`flock`,`board`,`continent`,`country`,`utag`,`user`,`bot`,`q`];
function _ssKey(p,kw){const src=new URLSearchParams(p instanceof URLSearchParams?p.toString():String(p||``)),o=new URLSearchParams();for(const k of _SS_KEYS){let v=k===`q`&&kw!=null?String(kw):src.get(k)||``;v=v.trim();if(v)o.set(k,v)}return o.toString()}
function _ssMe(){return(localStorage.getItem(`_myUsername`)||``).toLowerCase()}
const _SS={items:null,who:null,load(){const me=_ssMe();if(!me||!localStorage.getItem(`auth_token`))return[];if(this.who!==me){this.who=me;this.items=null}if(this.items)return this.items;try{const v=JSON.parse(localStorage.getItem(`pp_ss:`+me)||`null`);if(Array.isArray(v))this.items=v}catch(e){}return this.items||[]},
 set(list,send){const me=_ssMe();this.items=list;this.who=me;try{localStorage.setItem(`pp_ss:`+me,JSON.stringify(list))}catch(e){}dispatchEvent(new Event(`pp-ss`));if(send)fetch(`${R}/saved-searches`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({items:list})}).catch(()=>{})},
 _p:null,sync(){if(!localStorage.getItem(`auth_token`))return Promise.resolve([]);if(this._p)return this._p;this._p=fetch(`${R}/saved-searches`,{headers:{...er()}}).then(r=>r.ok?r.json():null).then(j=>{if(j&&Array.isArray(j.items))this.set(j.items,!1);return this.load()}).catch(()=>this.load()).finally(()=>{setTimeout(()=>{this._p=null},30000)});return this._p}};
function _ssUse(){const[,f]=(0,_.useState)(0);(0,_.useEffect)(()=>{const h=()=>f(x=>x+1);addEventListener(`pp-ss`,h);_SS.sync();return()=>removeEventListener(`pp-ss`,h)},[]);return _SS.load()}
function _ssDefault(params,go){try{if(!localStorage.getItem(`auth_token`)||location.pathname!==`/`)return;const now=Date.now(),last=+(sessionStorage.getItem(`pp_ss_at`)||0);sessionStorage.setItem(`pp_ss_at`,String(now));
 if(last&&now-last<30*60e3)return;const p=new URLSearchParams(params.toString());if([..._SS_KEYS,`time`,`sort`,`range`,`tab`].some(k=>p.get(k)))return;
 const t0=Date.now(),use=list=>{const d=(list||[]).find(x=>x.def);if(!d)return;if(location.pathname!==`/`||location.search)return;if(Date.now()-t0>4000)return;go(d.qs)};
 const have=_SS.load();if(have.length)use(have);else _SS.sync().then(use)}catch(e){}}
const _SS_IC={mark:`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4h12v16l-6-4.2L6 20z"/></svg>`,markOn:`<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4h12v16l-6-4.2L6 20z"/></svg>`,
 star:`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><path d="M12 3.5l2.6 5.3 5.9.9-4.2 4.1 1 5.8L12 16.9l-5.3 2.7 1-5.8-4.2-4.1 5.9-.9z"/></svg>`,starOn:`<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><path d="M12 3.5l2.6 5.3 5.9.9-4.2 4.1 1 5.8L12 16.9l-5.3 2.7 1-5.8-4.2-4.1 5.9-.9z"/></svg>`,
 x:`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>`};
function _ssPills(qs){const p=new URLSearchParams(qs),out=[],k=[];
 if(p.get(`flock`)===`1`)out.push((0,L.jsx)(Ar,{boardName:`Flock`,small:!0},`fk`));
 const b=p.get(`board`);if(b){const o=nr.find(e=>e.slug===b);out.push((0,L.jsx)(Ar,{boardName:o?o.name:b,small:!0},`b`))}
 const co=p.get(`country`),ct=p.get(`continent`);if(co)out.push((0,L.jsx)(kr,{country:co,small:!0},`c`));else if(ct)out.push((0,L.jsx)(kr,{continent:ct,small:!0},`r`));
 const ut=p.get(`utag`);if(ut)out.push((0,L.jsx)(_UTag,{tag:ut,small:!0},`u`));
 const us=p.get(`user`);if(us)out.push((0,L.jsx)(`span`,{className:`ss-kw`,style:{color:Hn(``,us),borderColor:Hn(``,us)},children:us},`us`));
 const bt=p.get(`bot`);if(bt)out.push((0,L.jsx)(`span`,{className:`ss-kw`,children:bt===`hide`?`No bots`:`Bots`},`bt`));
 const q=p.get(`q`);if(q&&!(co&&q.toLowerCase()===co.toLowerCase()))out.push((0,L.jsx)(`span`,{className:`ss-kw`,children:`“${q}”`},`q`));
 return out}
function _SaveSearchBtn({params,kw}){const list=_ssUse(),[pop,setPop]=(0,_.useState)(!1);if(!localStorage.getItem(`auth_token`))return null;
 const key=_ssKey(params,kw);if(!key)return null;const has=list.some(x=>x.qs===key);
 return(0,L.jsx)(`button`,{type:`button`,className:`ss-btn`+(has?` on`:``)+(pop?` pop`:``),"aria-label":has?`Remove this saved search`:`Save this search`,title:has?`Saved · tap to remove`:`Save this search`,
  onMouseDown:ev=>ev.preventDefault(),onClick:ev=>{ev.stopPropagation();ev.preventDefault();const cur=_SS.load();
   if(has){_SS.set(cur.filter(x=>x.qs!==key),!0);return}
   if(cur.length>=5){alert(`You can save up to 5 searches. Remove one in the Tags tab of the search menu.`);return}
   _SS.set([...cur,{qs:key,def:!1}],!0);setPop(!0);setTimeout(()=>setPop(!1),360)},
  dangerouslySetInnerHTML:{__html:has?_SS_IC.markOn:_SS_IC.mark}})}
function _SavedSearches({go}){const list=_ssUse(),[ed,setEd]=(0,_.useState)(!1);if(!localStorage.getItem(`auth_token`))return null;
 const star=qs=>_SS.set(_SS.load().map(x=>({...x,def:x.qs===qs?!x.def:!1})),!0),rm=qs=>{const n=_SS.load().filter(x=>x.qs!==qs);_SS.set(n,!0);if(!n.length)setEd(!1)};
 return(0,L.jsxs)(`div`,{className:`ss-wrap`,onMouseDown:ev=>ev.preventDefault(),children:[(0,L.jsxs)(`div`,{className:`ss-hd`,children:[(0,L.jsx)(`div`,{className:`search-section-label`,children:`Saved searches`}),list.length?(0,L.jsx)(`button`,{type:`button`,className:`ss-ed`,onClick:ev=>{ev.stopPropagation();setEd(v=>!v)},children:ed?`Done`:`Edit`}):null]}),
  list.length?(0,L.jsx)(`div`,{className:`ss-list`,children:list.map(x=>(0,L.jsxs)(`div`,{className:`ss-it`,children:[
   ed?(0,L.jsx)(`button`,{type:`button`,className:`ss-star`+(x.def?` on`:``),"aria-label":x.def?`Stop using as default`:`Use as default`,onClick:ev=>{ev.stopPropagation();star(x.qs)},dangerouslySetInnerHTML:{__html:x.def?_SS_IC.starOn:_SS_IC.star}}):null,
   (0,L.jsxs)(`button`,{type:`button`,className:`ss-go`,onClick:ev=>{ev.stopPropagation();if(ed)return;go(x.qs)},children:[!ed&&x.def?(0,L.jsx)(`span`,{className:`ss-defic`,title:`Default`,dangerouslySetInnerHTML:{__html:_SS_IC.starOn}},`d`):null,..._ssPills(x.qs)]}),
   ed?(0,L.jsx)(`button`,{type:`button`,className:`ss-x`,"aria-label":`Remove`,onClick:ev=>{ev.stopPropagation();rm(x.qs)},dangerouslySetInnerHTML:{__html:_SS_IC.x}}):null]},x.qs))}):
  (0,L.jsx)(`div`,{className:`ss-none`,children:[`Pick some tags, then tap `,(0,L.jsx)(`span`,{style:{display:`inline-flex`,width:13,height:13,verticalAlign:`-2px`,color:`#94a3b8`},dangerouslySetInnerHTML:{__html:_SS_IC.mark}}),` in the search bar to save them here.`]}),
  ed?(0,L.jsx)(`div`,{className:`ss-none`,children:`Star one to fill your search bar when you open Perch Posts.`}):null]})}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
