#!/usr/bin/env python3
"""Patch v1122 -> v1123: giving worms only happens on purpose, and you can see who gave them.
- Post Reactions view: a 🪱 tab (always there); the Give worms row lives in that tab. The 🪱 pill next to the bird
  opens straight on it.
- Chirps: tapping the 🪱 pill no longer gives a worm. It opens the who-reacted sheet on a 🪱 tab listing who gave worms
  (and how many), with the Give worms row.
- The emoji picker ("+" in a chirp's reaction bar) gets a 🪱 tab to the left of the emoji (it still opens on the emoji)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1122.js'
dst = '_deploy/assets/index-DUcNPOLc-v1123.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# give row works for chirps too
patch("function _WormGive({id}){", "function _WormGive({id,kind=`p`}){", 'give row: any kind')
patch("_ppWorm.give(`p`,id,k);setN(1);", "_ppWorm.give(kind,id,k);setN(1);", 'give row gives that kind')

# post Reactions view: 🪱 tab always there, give row inside it
i = c.index("function _PostReactions({id}){"); j = c.index("// the small pill next to the bird on the post page", i)
c = c[:i] + r'''const _prxStart=new Map();
function _WormGivers({kind,id,go}){const[g,set]=(0,_.useState)(null);
 (0,_.useEffect)(()=>{let on=!0;const ld=()=>fetch(`${R}/worm-givers?${kind===`c`?`comment_id`:`post_id`}=${encodeURIComponent(id)}`,{headers:er()}).then(r=>r.ok?r.json():{givers:[]}).then(d=>on&&set(d.givers||[])).catch(()=>on&&set([]));
  ld();const u=_ppWorm.sub(_ppWorm.key(kind,id),()=>setTimeout(ld,600));return()=>{on=!1;u()}},[kind,id]);
 return(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(_WormGive,{id,kind}),!g?(0,L.jsx)(`div`,{className:`cp-empty`,children:`Loading…`}):!g.length?(0,L.jsx)(`div`,{className:`cp-empty`,children:`No worms yet`}):
  g.map(p=>{const f=_rxFace(p.username,16),k=f.col,tap=go&&p.username!==`Extinct Bird`;return(0,L.jsxs)(`div`,{className:`rx-row${tap?` tap`:``}`,onClick:tap?ev=>{ev.stopPropagation();go(p.username)}:void 0,style:{background:`color-mix(in srgb, ${k} 9%, #15171d)`,borderColor:`color-mix(in srgb, ${k} 22%, transparent)`},children:[
   (0,L.jsx)(`span`,{className:`rx-av`,style:{background:`color-mix(in srgb, ${k} 24%, #1b1d24)`,borderColor:`color-mix(in srgb, ${k} 40%, transparent)`},children:f.el}),
   (0,L.jsx)(`span`,{className:`rx-nm`,style:{color:k===`#ffffff`?`#e5e7eb`:k},children:p.username}),
   (0,L.jsxs)(`span`,{className:`pr-did`,children:[(0,L.jsxs)(`span`,{className:`pr-w`,children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),p.c]})]})]},p.username)})]})}
function _PostReactions({id}){const ppl=_usePrx(id),[tab,setTab]=(0,_.useState)(()=>{const s=_prxStart.get(id);_prxStart.delete(id);return s||`all`});
 (0,_.useEffect)(()=>{const s=_prxStart.get(id);if(s){_prxStart.delete(id);setTab(s)}});
 const ic=k=>(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(k)}});
 const T=(k,ch)=>(0,L.jsx)(`button`,{type:`button`,className:`pr-tab`+(tab===k?` on`:``),onClick:ev=>{ev.stopPropagation();setTab(k)},children:ch},k);
 const list=ppl||[],nf=list.filter(p=>p.flap).length,nw=list.reduce((s,p)=>s+(p.worms||0),0);
 const show=list.filter(p=>tab===`all`||(tab===`flap`&&p.flap));
 const row=p=>{const f=_rxFace(p.username,16),k=f.col;return(0,L.jsxs)(`div`,{className:`rx-row`,"data-gpb":p.username,style:{background:`color-mix(in srgb, ${k} 9%, #15171d)`,borderColor:`color-mix(in srgb, ${k} 22%, transparent)`},children:[
   (0,L.jsx)(`span`,{className:`rx-av`,style:{background:`color-mix(in srgb, ${k} 24%, #1b1d24)`,borderColor:`color-mix(in srgb, ${k} 40%, transparent)`},children:f.el}),
   (0,L.jsx)(`span`,{className:`rx-nm`,style:{color:k===`#ffffff`?`#e5e7eb`:k},children:p.username}),
   (0,L.jsxs)(`span`,{className:`pr-did`,children:[p.flap?ic(`BIRD`):null,p.worms?(0,L.jsxs)(`span`,{className:`pr-w`,children:[ic(`WORM`),p.worms]}):null]})]},p.username)};
 return(0,L.jsxs)(`div`,{className:`pr-wrap`,onClick:ev=>ev.stopPropagation(),children:[
  (0,L.jsxs)(`div`,{className:`pr-tabs`,children:[T(`all`,`All ${list.length}`),T(`flap`,[ic(`BIRD`),nf]),T(`worm`,[ic(`WORM`),nw])]}),
  tab===`worm`?(0,L.jsx)(_WormGivers,{kind:`p`,id}):!ppl?(0,L.jsx)(`div`,{className:`cp-empty`,children:`Loading…`}):!show.length?(0,L.jsx)(`div`,{className:`cp-empty`,children:tab===`flap`?`No flaps yet`:`No flaps or worms yet`}):(0,L.jsx)(`div`,{className:`pr-list`,children:show.map(row)})]})}
''' + c[j:]; print('OK: post Reactions view with a worm tab')
# the 🪱 pill next to the bird opens straight on the worm tab
patch("onClick:ev=>{ev.preventDefault();ev.stopPropagation();if(pv){setCpm(`react`);", "onClick:ev=>{ev.preventDefault();ev.stopPropagation();_prxStart.set(id,`worm`);if(pv){setCpm(`react`);", 'pill opens the worm tab')

# chirps: the worm pill opens the sheet instead of giving
patch("function _WormPill({k,id,chirp,solo}){", "function _WormPill({k,id,chirp,solo,onOpen}){", 'pill can open')
patch("onClick:ev=>{ev.preventDefault();ev.stopPropagation();const el=ev.currentTarget;if(_ppWorm.give(k,id)){", "onClick:ev=>{ev.preventDefault();ev.stopPropagation();if(onOpen)return onOpen();const el=ev.currentTarget;if(_ppWorm.give(k,id)){", 'pill opens rather than gives')
patch("(0,L.jsx)(_WormPill,{k:`c`,id:e.id,chirp:1}),", "(0,L.jsx)(_WormPill,{k:`c`,id:e.id,chirp:1,onOpen:()=>_setRxW(`🪱`)}),", 'chirp pill opens sheet')
patch("(0,L.jsx)(_WormPill,{k:`c`,id:e.id,chirp:1,solo:1})", "(0,L.jsx)(_WormPill,{k:`c`,id:e.id,chirp:1,solo:1,onOpen:()=>_setRxW(`🪱`)})", 'solo chirp pill opens sheet')
# the who-reacted sheet: a 🪱 tab with who gave worms and the give row
patch("_rxW?_rxSheet(ee,_rxW,_setRxW,_rxGo):null", "_rxW?_rxSheet(ee,_rxW,_setRxW,_rxGo,e.id):null", 'sheet knows the chirp')
patch("function _rxSheet(ee,sel,set,go){const tot=ee.reduce((a,[,ids])=>a+ids.length,0),cur=sel===`all`||ee.some(([q])=>q===sel)?sel:`all`;",
      "function _rxSheet(ee,sel,set,go,cid){const tot=ee.reduce((a,[,ids])=>a+ids.length,0),cur=sel===`all`||(sel===`🪱`&&cid)||ee.some(([q])=>q===sel)?sel:`all`;", 'sheet worm tab selectable')
patch("(0,L.jsxs)(`div`,{className:`rx-tabs`,children:[tab(`all`,`All ${tot}`),..._rxSort(ee).map(([q,ids])=>tab(q,`${q} ${ids.length}`))]}),\n  (0,L.jsx)(`div`,{className:`rx-list`,children:_rxGroup(ee,cur).map((r,i)=>_rxRow(r,i,0,0,go?n=>{set(null);go(n)}:null))})]})})}",
      "(0,L.jsxs)(`div`,{className:`rx-tabs`,children:[tab(`all`,`All ${tot}`),cid?tab(`🪱`,[(0,L.jsx)(`span`,{className:`pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}},`i`),` `+_ppWorm.n(_ppWorm.key(`c`,cid))]):null,..._rxSort(ee).map(([q,ids])=>tab(q,`${q} ${ids.length}`))]}),\n"
      "  (0,L.jsx)(`div`,{className:`rx-list`,children:cur===`🪱`?(0,L.jsx)(_WormGivers,{kind:`c`,id:cid,go:go?n=>{set(null);go(n)}:null}):_rxGroup(ee,cur).map((r,i)=>_rxRow(r,i,0,0,go?n=>{set(null);go(n)}:null))})]})})}", 'sheet worm tab')

# emoji picker: a 🪱 tab to the left of the emoji (opens on the emoji)
patch("function _rxPick(cb){", "function _rxPick(cb,wo){", 'picker takes a worm target')
patch(" sh.append(hd,host,kb);ov.append(sh);\n let shut=!1;",
      " sh.append(hd,host,kb);ov.append(sh);\n let shut=!1;\n"
      " if(wo){const tb=document.createElement(`div`);tb.className=`rx-pick-tabs`;const tw=document.createElement(`button`),te=document.createElement(`button`);tw.type=te.type=`button`;\n"
      "  tw.className=`rx-pick-tab`;tw.innerHTML=`<span class=\"pp-ic\">${_ppIco(`WORM`)}</span>Worms`;te.className=`rx-pick-tab on`;te.innerHTML=`<span class=\"pp-ic\">${_ppIco(`CLOCK`)}</span>Emoji`;tb.append(tw,te);sh.insertBefore(tb,host);\n"
      "  const wp=document.createElement(`div`);wp.className=`rx-pick-worms`;wp.hidden=!0;sh.insertBefore(wp,host);let cnt=1,bal=_ppWorm.bal();\n"
      "  wp.innerHTML=`<div class=\"pp-pick-worm\"><span class=\"pp-ic pp-worm\">${_ppIco(`WORM`)}</span><span class=\"pp-pick-wl\">Give worms</span><button type=\"button\" class=\"pp-pick-st\" aria-label=\"Fewer\">−</button><b class=\"pp-pick-n\">1</b><button type=\"button\" class=\"pp-pick-st\" aria-label=\"More\">+</button><button type=\"button\" class=\"pp-pick-give\">Give 1</button></div><div class=\"pp-pick-bal\"></div>`;\n"
      "  const[mn,pl]=wp.querySelectorAll(`.pp-pick-st`),nb=wp.querySelector(`.pp-pick-n`),gv=wp.querySelector(`.pp-pick-give`),bl=wp.querySelector(`.pp-pick-bal`);\n"
      "  const upd=()=>{if(bal!=null&&cnt>Math.max(1,bal))cnt=Math.max(1,bal);nb.textContent=cnt;gv.textContent=`Give ${cnt}`;gv.disabled=bal===0;pl.disabled=bal!=null&&cnt>=bal;mn.disabled=cnt<=1;bl.textContent=bal==null?`Counting your worms…`:bal===0?`You don't have any worms to give`:`You have ${bal} worm${bal===1?``:`s`}`};upd();\n"
      "  mn.onclick=()=>{cnt=Math.max(1,cnt-1);upd()};pl.onclick=()=>{cnt=Math.min(50,bal==null?cnt+1:Math.min(bal,cnt+1));upd()};gv.onclick=()=>{if(bal===0)return;_ppWorm.give(wo.kind,wo.id,cnt);close()};\n"
      "  const show=w=>{tw.classList.toggle(`on`,w);te.classList.toggle(`on`,!w);wp.hidden=!w;host.style.display=kb.style.display=w?`none`:``;if(w)_ppWorm.loadBal().then(v=>{bal=v;upd()})};tw.onclick=()=>show(!0);te.onclick=()=>show(!1)}", 'picker worm tab')
patch("_rxPick(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)})", "_rxPick(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)},{kind:`c`,id})", 'chirp picker gets the worm tab')

# phone emoji sheet (React): a 🪱 button first in the bottom row (it still opens on recents); picking the 🪱 emoji goes there too
WROW = ("<div class=\"pp-pick-worm\"><span class=\"pp-ic pp-worm\">${_ppIco(`WORM`)}</span><span class=\"pp-pick-wl\">Give worms</span><button type=\"button\" class=\"pp-pick-st\" aria-label=\"Fewer\">−</button><b class=\"pp-pick-n\">1</b><button type=\"button\" class=\"pp-pick-st\" aria-label=\"More\">+</button><button type=\"button\" class=\"pp-pick-give\">Give 1</button></div><div class=\"pp-pick-bal\"></div>")
patch("function _rxIos(cb,_src){", "function _rxIos(cb,_src,wo){", 'emoji sheet takes a worm target')
patch(" const sh=ov.firstChild,inp=ov.querySelector(`input`),sc=ov.querySelector(`.ri-scroll`),nav=ov.querySelector(`.ri-nav`);",
      " const sh=ov.firstChild,inp=ov.querySelector(`input`),sc=ov.querySelector(`.ri-scroll`),nav=ov.querySelector(`.ri-nav`);\n"
      " let showW=()=>{};if(wo){const wb=document.createElement(`button`);wb.type=`button`;wb.className=`ri-cat ri-wcat`;wb.dataset.cat=`__worm`;wb.setAttribute(`aria-label`,`Worms`);wb.innerHTML=_ppIco(`WORM`);nav.prepend(wb);\n"
      "  const wp=document.createElement(`div`);wp.className=`ri-worms`;wp.hidden=!0;wp.innerHTML=`" + WROW + "`;sc.parentNode.insertBefore(wp,sc);let cnt=1,bal=_ppWorm.bal();\n"
      "  const[mn,pl]=wp.querySelectorAll(`.pp-pick-st`),nb=wp.querySelector(`.pp-pick-n`),gv=wp.querySelector(`.pp-pick-give`),bl=wp.querySelector(`.pp-pick-bal`);\n"
      "  const upd=()=>{if(bal!=null&&cnt>Math.max(1,bal))cnt=Math.max(1,bal);nb.textContent=cnt;gv.textContent=`Give ${cnt}`;gv.disabled=bal===0;pl.disabled=bal!=null&&cnt>=bal;mn.disabled=cnt<=1;bl.textContent=bal==null?`Counting your worms…`:bal===0?`You don't have any worms to give`:`You have ${bal} worm${bal===1?``:`s`}`};upd();\n"
      "  mn.onclick=()=>{cnt=Math.max(1,cnt-1);upd()};pl.onclick=()=>{cnt=Math.min(50,bal==null?cnt+1:Math.min(bal,cnt+1));upd()};gv.onclick=()=>{if(bal===0)return;_ppWorm.give(wo.kind,wo.id,cnt);close()};\n"
      "  showW=w=>{wp.hidden=!w;sc.style.display=w?`none`:``;wb.classList.toggle(`on`,w);if(w){nav.querySelectorAll(`.ri-cat:not(.ri-wcat)`).forEach(b=>b.classList.remove(`on`));_ppWorm.loadBal().then(v=>{bal=v;upd()})}}}", 'worm button in the emoji sheet')
patch(" sc.addEventListener(`click`,e=>{const b=e.target.closest(`.ri-e`);if(!b)return;const q=b.dataset.e;_riUse(q);close();cb(q)});",
      " sc.addEventListener(`click`,e=>{const b=e.target.closest(`.ri-e`);if(!b)return;const q=b.dataset.e;if(q===`🪱`&&wo){showW(!0);return}_riUse(q);close();cb(q)});", '🪱 emoji opens the worm tab')
patch(" nav.addEventListener(`click`,e=>{const b=e.target.closest(`.ri-cat`);if(!b)return;if(inp.value.trim()){inp.value=``;draw()}",
      " nav.addEventListener(`click`,e=>{const b=e.target.closest(`.ri-cat`);if(!b)return;if(b.dataset.cat===`__worm`){showW(!0);return}showW(!1);if(inp.value.trim()){inp.value=``;draw()}", 'emoji buttons leave the worm tab')
patch(" _rxIos(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)},_src)}", " _rxIos(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)},_src,{kind:`c`,id})}", 'React passes the chirp')
# computer picker: picking the 🪱 emoji opens its worm tab
patch(" const done=q=>{close();cb(q)};", " let _wTab=null;const done=q=>{if(q===`🪱`&&_wTab){_wTab();return}close();cb(q)};", 'computer picker: 🪱 opens worms')
patch("tw.onclick=()=>show(!0);te.onclick=()=>show(!1)}", "tw.onclick=()=>show(!0);te.onclick=()=>show(!1);_wTab=()=>show(!0)}", 'computer picker worm hook')
# no silent worm from a 🪱 reaction any more (worms only through the Give buttons)
patch("async function ne(e,t){if(t===`🪱`){_ppWorm.give(`c`,e);return}", "async function ne(e,t){if(t===`🪱`)return;", 'no silent worm')

css = ("body .rx-pick-tabs{display:flex;gap:6px;padding:0 12px 8px}"
       "body .rx-pick-tab{display:inline-flex;align-items:center;gap:5px;height:30px;padding:0 12px;border-radius:999px;border:1px solid rgba(148,163,184,.22);background:rgba(148,163,184,.06);color:#94a3b8;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit}"
       "body .rx-pick-tab.on{background:#c084fc;border-color:#c084fc;color:#14081d}body .rx-pick-tab .ri{width:15px;height:15px;stroke-width:2.2;display:block}body .rx-pick-tab .ri.wemo{font-size:13px}"
       "body .rx-pick-worms{padding:6px 12px 14px}body .rx-pick-worms .pp-pick-worm{border-top:0}"
       "body .ri-worms{padding:10px 14px 8px}body .ri-worms .pp-pick-worm{border-top:0}body .ri-wcat .ri.wemo{font-size:19px}"
       "body .rx-tab .pp-ic{display:inline-flex;vertical-align:-1px}body .rx-tab .ri.wemo{font-size:12px}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
