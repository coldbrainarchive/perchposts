#!/usr/bin/env python3
"""Patch v1148 -> v1149: post flaps & worms open right under the post (like chirp reactions), no tabs.
- Flap pill: the icon flaps; the number opens "who flapped" under the post.
- Worm pill (shown once worms exist): opens "who gave worms" under the post.
- "+🪱" button on people's posts (not your own, not bots): opens the worm list with the give row.
- The list has a "Give worms" link (expands the give row). The tapped pill is highlighted; tapping again closes.
- "Flaps & worms" leaves the chirp menu. Notifications / card worm pills open the right list under the post."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1148.js'
dst = '_deploy/assets/index-DUcNPOLc-v1149.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

COMP = r'''const _ppPP=(()=>{let v=null;const s=new Set(),em=()=>s.forEach(f=>{try{f()}catch(e){}});return{get:()=>v,set:x=>{v=x;em()},toggle:(id,k)=>{v=v&&v.id===id&&(v.k===k||k===`w`&&v.k===`g`)?null:{id,k};em()},sub:f=>{s.add(f);return()=>s.delete(f)}}})();
function _usePP(){const[,f]=(0,_.useState)(0);(0,_.useEffect)(()=>_ppPP.sub(()=>f(x=>x+1)),[]);return _ppPP.get()}
function _FlapCount({id,n}){const pp=_usePP(),on=!!pp&&pp.id===id&&pp.k===`f`;
 return(0,L.jsx)(`span`,{className:`pp-fcount`+(on?` sel`:``),role:`button`,"aria-label":`See who flapped`,onClick:ev=>{ev.preventDefault();ev.stopPropagation();_ppPP.toggle(id,`f`)},children:n})}
function _PostWormPill({id}){const pp=_usePP(),ppl=_usePrx(id),nw=(ppl||[]).reduce((s,p)=>s+(p.worms||0),0);(0,_.useEffect)(()=>{_ppWorm.want(`p`,id)},[id]);
 if(!nw)return null;const on=!!pp&&pp.id===id&&(pp.k===`w`||pp.k===`g`);
 return(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill pr-line`+(on?` sel`:``),title:`Who gave worms`,onClick:ev=>{ev.preventDefault();ev.stopPropagation();_ppPP.toggle(id,`w`)},children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),nw]})}
function _PostGiveBtn({id}){const pp=_usePP(),on=!!pp&&pp.id===id&&pp.k===`g`;
 return(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill pp-give`+(on?` sel`:``),"aria-label":`Give worms`,title:`Give worms`,onClick:ev=>{ev.preventDefault();ev.stopPropagation();_ppPP.toggle(id,`g`)},children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),`+`]})}
function _PostPanel({id,bot}){const pp=_usePP(),ppl=_usePrx(id),ref=(0,_.useRef)(null),[gv,setGv]=(0,_.useState)(!1),open=!!pp&&pp.id===id;
 (0,_.useEffect)(()=>{setGv(!!pp&&pp.id===id&&pp.k===`g`)},[pp&&pp.id,pp&&pp.k]);
 const hl=()=>{const h=window._ppRxHL;if(!h||h.id!==id||!ppl)return;window._ppRxHL=null;setTimeout(()=>{const w=ref.current;if(!w)return;const el=[...w.querySelectorAll(`.rx-row`)].find(x=>x.dataset.gpb===h.u);if(!el)return;
  el.scrollIntoView({behavior:`smooth`,block:`center`});const nm=el.querySelector(`.rx-nm`),m=nm&&getComputedStyle(nm).color.match(/(\d+),\s*(\d+),\s*(\d+)/);el.style.setProperty(`--gc`,m?`${m[1]},${m[2]},${m[3]}`:`192,132,252`);
  clearTimeout(el._gt);el.classList.remove(`chat-flash`);void el.offsetWidth;el.classList.add(`chat-flash`);el._gt=setTimeout(()=>el.classList.remove(`chat-flash`),2600)},300)};
 (0,_.useEffect)(hl,[open,pp&&pp.k,ppl]);(0,_.useEffect)(()=>{const f=()=>hl();addEventListener(`pp-rx-hl`,f);return()=>removeEventListener(`pp-rx-hl`,f)},[ppl]);
 if(!open)return null;
 const kd=pp.k===`f`?`f`:`w`,list=(ppl||[]).filter(p=>kd===`f`?p.flap:p.worms>0);
 const ic=k=>(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(k)}});
 const row=p=>{const f=_rxFace(p.username,16),k=f.col;return(0,L.jsxs)(`div`,{className:`rx-row`,"data-gpb":p.username,"data-kd":kd,style:{background:`color-mix(in srgb, ${k} 9%, #15171d)`,borderColor:`color-mix(in srgb, ${k} 22%, transparent)`},children:[
   (0,L.jsx)(`span`,{className:`rx-av`,style:{background:`color-mix(in srgb, ${k} 24%, #1b1d24)`,borderColor:`color-mix(in srgb, ${k} 40%, transparent)`},children:f.el}),
   (0,L.jsx)(`span`,{className:`rx-nm`,style:{color:k===`#ffffff`?`#e5e7eb`:k},children:p.username}),
   (0,L.jsx)(`span`,{className:`pr-did`,children:kd===`f`?ic(`BIRD`):(0,L.jsxs)(`span`,{className:`pr-w`,children:[ic(`WORM`),p.worms]})})]},p.username+kd)};
 return(0,L.jsxs)(`div`,{className:`pp-panel pr-wrap`,ref,onClick:ev=>ev.stopPropagation(),children:[
  !ppl?(0,L.jsx)(`div`,{className:`cp-empty`,children:`Loading…`}):list.length?(0,L.jsx)(`div`,{className:`pr-list`+(list.length>5?` rx-scroll`:``),onScroll:_rxEnd,children:list.map(row)}):(0,L.jsx)(`div`,{className:`cp-empty`,children:kd===`f`?`No flaps yet`:`No worms yet`}),
  bot?null:gv?(0,L.jsx)(_WormGive,{id,kind:`p`,bare:1}):(0,L.jsxs)(`button`,{type:`button`,className:`wg-open pp-give-link`,onClick:ev=>{ev.stopPropagation();setGv(!0)},children:[`Give worms`,(0,L.jsx)(`span`,{className:`wg-chev`,children:`⌄`})]})]})}
'''
patch("function _PFTabs({u,on}){", COMP + "function _PFTabs({u,on}){", 'components')
# flap pill: number opens the list
patch("children:[(0,L.jsx)(`span`,{className:`pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),(0,L.jsx)(`span`,{children:re.score})]}),!c?.is_huddle&&c&&(0,L.jsx)(_PostRespLine,{id:c.id,pv:_pv,setCpm:_setCpm}),",
      "children:[(0,L.jsx)(`span`,{className:`pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),(0,L.jsx)(_FlapCount,{id:c.id,n:re.score})]}),"
      "!c?.is_huddle&&c&&(0,L.jsx)(_PostWormPill,{id:c.id}),!c?.is_huddle&&c&&!c.frozen&&!_ppIsBot(c)&&!_ppOwn(c.username)&&(0,L.jsx)(_PostGiveBtn,{id:c.id}),!c?.is_huddle&&c&&(0,L.jsx)(_PostPanel,{id:c.id,bot:_ppIsBot(c)||_ppOwn(c.username)}),",
      'post action row')
# chirp menu: no Flaps & worms
patch("const _CPL={react:`🪽 Flaps & worms`,hl:", "const _CPL={hl:", 'menu back to chirps only')
# arriving with ?rx / from a card worm pill: open the list under the post
patch("_setCpm((_ppRxOpen.delete(r)||_rk)?(setTimeout(()=>document.querySelector(`.comments-shell`)?.scrollIntoView({behavior:`smooth`,block:`start`}),450),`react`):`hl`);",
      "{const _o=_ppRxOpen.delete(r)||_rk;_setCpm(`hl`);if(_o){_ppPP.set({id:r,k:_rk||`w`});setTimeout(()=>document.querySelector(`.pp-panel`)?.scrollIntoView({behavior:`smooth`,block:`center`}),600)}else if(_ppPP.get()&&_ppPP.get().id!==r)_ppPP.set(null)}",
      'arrival opens the panel')
patch("window._ppRxHL=d;if(_cf)_closeC();_setCpm(`react`);setTimeout(()=>{document.querySelector(`.comments-shell`)?.scrollIntoView({behavior:`smooth`,block:`start`});dispatchEvent(new CustomEvent(`pp-rx-hl`))},350)",
      "window._ppRxHL=d;if(_cf)_closeC();_ppPP.set({id:r,k:d.k});setTimeout(()=>{document.querySelector(`.pp-panel`)?.scrollIntoView({behavior:`smooth`,block:`center`});dispatchEvent(new CustomEvent(`pp-rx-hl`))},350)",
      'same-post notification opens the panel')
css = ("body .feed-post-actions:has(> .pp-panel){flex-wrap:wrap}body .pp-panel{order:99;flex-basis:100%;margin-top:10px;padding:0}"
       "body .pp-panel .pr-list{margin:0}body .pp-panel .cp-empty{padding:10px 4px;text-align:left}"
       "body .pp-give-link{border:0;background:none;padding:8px 4px 0;height:auto;color:#fda4af;margin:0}"
       "body .pp-panel .wg-row{margin:10px 0 0}"
       "body .pp-fcount{margin:-6px -10px -6px 0;padding:6px 10px 6px 6px;border-left:1px solid rgba(148,163,184,.22);border-radius:0 999px 999px 0;cursor:pointer}"
       "body .pp-fcount.sel{background:rgba(192,132,252,.25);color:#f3e8ff}"
       "body .feed-post-action-pill.pr-line.sel,body .feed-post-action-pill.pp-give.sel{border-color:#c084fc!important;background:rgba(192,132,252,.18)!important}"
       "body .pp-give{gap:2px;font-weight:800;color:#fda4af}body .pp-give .ri.wemo{font-size:14px}"
       "body .pp-panel .pr-did svg.ri{width:22px!important;height:22px!important;stroke-width:2.7}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
