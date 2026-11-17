#!/usr/bin/env python3
"""Patch v1148 -> v1151 (v1149, v1150 were unreleased drafts): one-tap flap; a worm pill (shows 0 too) opens the
"Worm wallet" under the post: your balance + give row, who gave worms, who flapped.
- The flap pill (whole pill) and the worm pill (shown once worms exist) open one panel under the post; tapping the
  other pill switches the list (who flapped / who gave worms); tapping the open one closes it.
- The panel starts with "+ Flap" (or "Flapped", tap to undo) and "+ Give worms" (opens the give row), then the list.
  No flap / worm buttons on your own post; no worms on bot posts.
- "Flaps & worms" leaves the chirp menu. Notifications / card worm pills open the panel on the right list."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1148.js'
dst = '_deploy/assets/index-DUcNPOLc-v1151.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

COMP = r'''const _ppPP=(()=>{let v=null;const s=new Set(),em=()=>s.forEach(f=>{try{f()}catch(e){}});return{get:()=>v,set:x=>{v=x;em()},toggle:(id,k)=>{v=v&&v.id===id&&v.k===k?null:{id,k};em()},sub:f=>{s.add(f);return()=>s.delete(f)}}})();
function _usePP(){const[,f]=(0,_.useState)(0);(0,_.useEffect)(()=>_ppPP.sub(()=>f(x=>x+1)),[]);return _ppPP.get()}
function _useResp(id){const[,f]=(0,_.useState)(0);(0,_.useEffect)(()=>_ppResp.sub(id,()=>f(x=>x+1)),[id]);return _ppResp.get(id)}
function _PostFlapPill({id,score,mine}){const pp=_usePP(),o=_useResp(id),n=o&&o.n!=null?o.n:score,m=o&&o.n!=null?o.m:mine,on=!!pp&&pp.id===id&&pp.k===`f`;
 return(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill pp-flap`+(on?` sel`:``)+(m===1?` mine`:``),"aria-label":`Flaps: ${n}`,"aria-expanded":on,onClick:ev=>{ev.preventDefault();ev.stopPropagation();_ppPP.toggle(id,`f`)},children:[(0,L.jsx)(`span`,{className:`pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),(0,L.jsx)(`span`,{children:n})]})}
function _PostWormPill({id}){const pp=_usePP(),ppl=_usePrx(id),nw=(ppl||[]).reduce((s,p)=>s+(p.worms||0),0);(0,_.useEffect)(()=>{_ppWorm.want(`p`,id)},[id]);
 const on=!!pp&&pp.id===id;
 return(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill pr-line`+(on?` sel`:``),"aria-label":`Worms: ${nw}`,"aria-expanded":on,onClick:ev=>{ev.preventDefault();ev.stopPropagation();_ppPP.toggle(id,`w`)},children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),nw]})}
async function _ppFlapPost(id,frozen,own){if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}if(frozen)return;if(own){_ppOwnMsg();return}
 const o=_ppResp.get(id)||{n:0,m:0},nv=o.m===1?0:1;_ppResp.set(id,{n:nv?(o.n||0)+1:Math.max(0,(o.n||0)-1),m:nv?1:0});_lastVoteTs=Date.now();
 if(nv)setTimeout(()=>{try{_ppFlapAnim(document.querySelector(`.pp-flap`))}catch(e){}},30);
 const r=await Tr(id,nv).catch(()=>null);if(!r||!r.success){_ppResp.set(id,o);try{_hxToast(r&&r.error||`Could not flap`)}catch(e){}}}
function _PostPanel({id,own,frozen}){const pp=_usePP(),ppl=_usePrx(id),ref=(0,_.useRef)(null),open=!!pp&&pp.id===id;
 const hl=()=>{const h=window._ppRxHL;if(!h||h.id!==id||!ppl)return;window._ppRxHL=null;setTimeout(()=>{const w=ref.current;if(!w)return;const el=[...w.querySelectorAll(`.rx-row[data-kd="${h.k}"]`)].find(x=>x.dataset.gpb===h.u);if(!el)return;
  el.scrollIntoView({behavior:`smooth`,block:`center`});const nm=el.querySelector(`.rx-nm`),m=nm&&getComputedStyle(nm).color.match(/(\d+),\s*(\d+),\s*(\d+)/);el.style.setProperty(`--gc`,m?`${m[1]},${m[2]},${m[3]}`:`192,132,252`);
  clearTimeout(el._gt);el.classList.remove(`chat-flash`);void el.offsetWidth;el.classList.add(`chat-flash`);el._gt=setTimeout(()=>el.classList.remove(`chat-flash`),2600)},300)};
 (0,_.useEffect)(hl,[open,ppl]);(0,_.useEffect)(()=>{const f=()=>hl();addEventListener(`pp-rx-hl`,f);return()=>removeEventListener(`pp-rx-hl`,f)},[ppl]);
 if(!open)return null;
 const ic=k=>(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(k)}});
 const row=(p,kd)=>{const f=_rxFace(p.username,16),k=f.col;return(0,L.jsxs)(`div`,{className:`rx-row`,"data-gpb":p.username,"data-kd":kd,style:{background:`color-mix(in srgb, ${k} 9%, #15171d)`,borderColor:`color-mix(in srgb, ${k} 22%, transparent)`},children:[
   (0,L.jsx)(`span`,{className:`rx-av`,style:{background:`color-mix(in srgb, ${k} 24%, #1b1d24)`,borderColor:`color-mix(in srgb, ${k} 40%, transparent)`},children:f.el}),
   (0,L.jsx)(`span`,{className:`rx-nm`,style:{color:k===`#ffffff`?`#e5e7eb`:k},children:p.username}),
   (0,L.jsx)(`span`,{className:`pr-did`,children:kd===`f`?ic(`BIRD`):(0,L.jsxs)(`span`,{className:`pr-w`,children:[ic(`WORM`),p.worms]})})]},p.username+kd)};
 const worms=(ppl||[]).filter(p=>p.worms>0),flaps=(ppl||[]).filter(p=>p.flap);
 const sec=(title,list,kd,empty)=>[(0,L.jsx)(`div`,{className:`pp-list-h`,children:title},`h`+kd),!ppl?(0,L.jsx)(`div`,{className:`cp-empty`,children:`Loading…`},`l`+kd):list.length?(0,L.jsx)(`div`,{className:`pr-list`+(list.length>5?` rx-scroll`:``),onScroll:_rxEnd,children:list.map(p=>row(p,kd))},`r`+kd):(0,L.jsx)(`div`,{className:`cp-empty`,children:empty},`e`+kd)];
 return(0,L.jsxs)(`div`,{className:`pp-panel pr-wrap`,ref,onClick:ev=>ev.stopPropagation(),children:[
  (0,L.jsxs)(`div`,{className:`pp-wallet-h`,children:[ic(`WORM`),`Worm wallet`]}),
  !own&&!frozen?(0,L.jsx)(_WormGive,{id,kind:`p`,bare:1}):null,
  ...sec(`Who gave worms`,worms,`w`,own?`No worms yet`:`No worms yet. Be the first!`),
  ...(flaps.length?sec(`Who flapped`,flaps,`f`,``):[])]})}
'''
patch("function _PFTabs({u,on}){", COMP + "function _PFTabs({u,on}){", 'components')

patch("!c?.is_huddle&&c&&(0,L.jsx)(_PostRespLine,{id:c.id,pv:_pv,setCpm:_setCpm}),",
      "!c?.is_huddle&&c&&!_ppIsBot(c)&&(0,L.jsx)(_PostWormPill,{id:c.id},`wp`),!c?.is_huddle&&c&&!_ppIsBot(c)&&(0,L.jsx)(_PostPanel,{id:c.id,own:_ppOwn(c.username),frozen:!!c.frozen},`pnl`),",
      'post action row: one-tap flap, worm pill, wallet')

patch("const o=(p||{})[id]||{n:0,m:0};_ppResp.set(id,{n:o.n,m:o.m,emoji:o.emoji||null});", "const o=(p||{})[id]||{n:0,m:0};if(Date.now()-_lastVoteTs>3000||!_ppResp.get(id))_ppResp.set(id,{n:o.n,m:o.m,emoji:o.emoji||null});", 'refresh does not undo a fresh flap')
patch("const _CPL={react:`🪽 Flaps & worms`,hl:", "const _CPL={hl:", 'menu back to chirps only')
patch("_setCpm((_ppRxOpen.delete(r)||_rk)?(setTimeout(()=>document.querySelector(`.comments-shell`)?.scrollIntoView({behavior:`smooth`,block:`start`}),450),`react`):`hl`);",
      "{const _o=_ppRxOpen.delete(r)||_rk;_setCpm(`hl`);if(_o){_ppPP.set({id:r,k:_rk||`w`});setTimeout(()=>document.querySelector(`.pp-panel`)?.scrollIntoView({behavior:`smooth`,block:`center`}),600)}else if(_ppPP.get()&&_ppPP.get().id!==r)_ppPP.set(null)}",
      'arrival opens the panel')
patch("window._ppRxHL=d;if(_cf)_closeC();_setCpm(`react`);setTimeout(()=>{document.querySelector(`.comments-shell`)?.scrollIntoView({behavior:`smooth`,block:`start`});dispatchEvent(new CustomEvent(`pp-rx-hl`))},350)",
      "window._ppRxHL=d;if(_cf)_closeC();_ppPP.set({id:r,k:d.k});setTimeout(()=>{document.querySelector(`.pp-panel`)?.scrollIntoView({behavior:`smooth`,block:`center`});dispatchEvent(new CustomEvent(`pp-rx-hl`))},350)",
      'same-post notification opens the panel')
css = ("body .feed-post-actions:has(> .pp-panel){flex-wrap:wrap}body .pp-panel{order:99;flex-basis:100%;margin-top:10px;padding:12px;border-radius:16px;background:rgba(148,163,184,.05);border:1px solid rgba(148,163,184,.14)}"
       "body .pp-flap{padding-left:4px}body .pp-flap.mine{border-color:#c084fc;background:rgba(192,132,252,.15)}"
       "body .feed-post-action-pill.pp-flap.sel,body .feed-post-action-pill.pr-line.sel{border-color:#c084fc!important;background:rgba(192,132,252,.28)!important;box-shadow:inset 0 0 0 1px #c084fc}"
       "body .pp-add{display:flex;gap:8px;margin-bottom:12px}"
       "body .pp-add-btn{flex:1;display:inline-flex;align-items:center;justify-content:center;gap:6px;height:38px;border-radius:999px;font:inherit;font-size:14px;font-weight:700;cursor:pointer}"
       "body .pp-add-btn b{font-size:16px;line-height:1}body .pp-add-btn svg.ri{width:20px!important;height:20px!important;stroke-width:2.6}body .pp-add-btn .ri.wemo{font-size:16px}"
       "body .pp-add-flap{border:1px solid rgba(192,132,252,.45);background:rgba(192,132,252,.1);color:#d8b4fe}body .pp-add-flap.on{background:#c084fc;border-color:#c084fc;color:#14081d}"
       "body .pp-add-worm{border:1px solid rgba(251,113,133,.45);background:rgba(251,113,133,.08);color:#fda4af}body .pp-add-worm.on{background:rgba(251,113,133,.2)}"
       "body .pp-panel .wg-row{margin:0 0 14px}body .pp-wallet-h{display:flex;align-items:center;gap:6px;font-size:14px;font-weight:800;color:#fda4af;margin:0 2px 10px}body .pp-wallet-h .ri.wemo{font-size:16px}body .pp-panel .pr-list+.pp-list-h,body .pp-panel .cp-empty+.pp-list-h{margin-top:14px}"
       "body .pp-list-h{font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#64748b;margin:0 2px 8px}"
       "body .pp-panel .pr-list{margin:0}body .pp-panel .cp-empty{padding:6px 2px;text-align:left}"
       "body .pp-panel .pr-did svg.ri{width:22px!important;height:22px!important;stroke-width:2.7}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
