#!/usr/bin/env python3
"""Patch v1127 -> v1128:
- Post cards show the 🪱 worm count next to the bird (like the post page). Tapping it opens the post on its Reactions.
- The bird number is flaps only now (worker); the post page's quick +1 on flap no longer assumes worm givers counted.
- Bird ID (Bird button card and your nest card) gets a Flaps row: flaps other people gave your posts.
- Chirps: worms are given only in the emoji picker; the chirp sheet's 🪱 tab just lists who gave.
- Posts: the Give worms row on the Reactions 🪱 tab is folded behind a "Give worms" button.
- Tapping a worm pill (post or chirp) opens Reactions on All.
- The post preview (the chirp preview with its menu, incl. Reactions) is on desktop too, not just phones."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1127.js'
dst = '_deploy/assets/index-DUcNPOLc-v1128.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# --- post cards: worm pill (a link to the post, opening its Reactions) ---
patch("function _PFTabs({u,on}){",
      r'''const _ppRxOpen=new Set();
function _CardWorm({id}){const K=_ppWorm.key(`p`,id),[,f]=(0,_.useState)(0);(0,_.useEffect)(()=>{_ppWorm.want(`p`,id);return _ppWorm.sub(K,()=>f(x=>x+1))},[K]);
 return(0,L.jsxs)(I,{to:`/post/${id}`,className:`feed-post-action-pill pp-worm-pill`+(_ppWorm.m(K)?` mine`:``),title:`See reactions`,onClick:ev=>{ev.stopPropagation();_ppRxOpen.add(id)},children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{children:_ppWorm.n(K)})]})}
function _PFTabs({u,on}){''', 'card worm pill component')
patch("children:[(0,L.jsx)(`span`,{className:`pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),(0,L.jsx)(`span`,{children:n})]}),(0,L.jsxs)(I,{to:`/post/${e.id}?chat=1&via=card`",
      "children:[(0,L.jsx)(`span`,{className:`pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),(0,L.jsx)(`span`,{children:n})]}),!(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsx)(_CardWorm,{id:e.id}),(0,L.jsxs)(I,{to:`/post/${e.id}?chat=1&via=card`",
      'card shows the worm pill')
# arriving from a card's worm pill: open the preview on Reactions
patch("_setCF(!1);_setCpm(`hl`);",
      "_setCF(!1);_setCpm(_ppRxOpen.delete(r)?(setTimeout(()=>document.querySelector(`.comments-shell`)?.scrollIntoView({behavior:`smooth`,block:`start`}),450),`react`):`hl`);",
      'post opens on Reactions from a card')

# --- the preview on desktop too ---
patch("let _pv=window.innerWidth<768&&!_cf&&", "let _pv=!_cf&&!(window.innerWidth>=768&&new URLSearchParams(location.search).get(`chat`)===`1`)&&", 'post preview on desktop')

# on a computer, "View all" shows the whole chat in the page column (?chat=1), as before, not the phone's full screen
patch("_openC=()=>{if(_cf)return;", "_openC=()=>{if(_cf)return;if(window.innerWidth>=768){o(location.pathname+`?chat=1`);return}", 'desktop View all stays in the column')

# --- flaps only: quick +1 ---
patch("re.score+(re.myVote?0:1)", "re.score+1", 'flap +1')

# --- open on All ---
patch("_prxStart.set(id,`worm`);", "", 'post pill opens All')
patch("onOpen:()=>_setRxW(`🪱`)", "onOpen:()=>_setRxW(`all`)", 'chirp pill opens All', 2)

# --- give rows: none on chirps, folded on posts ---
patch("function _WormGivers({kind,id,go}){const[g,set]=(0,_.useState)(null);",
      "function _WormGivers({kind,id,go,give}){const[g,set]=(0,_.useState)(null),[op,setOp]=(0,_.useState)(!1);", 'givers: give option')
patch("return(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(_WormGive,{id,kind}),!g?",
      "return(0,L.jsxs)(L.Fragment,{children:[give?(0,L.jsxs)(`button`,{type:`button`,className:`wg-open`+(op?` on`:``),\"aria-expanded\":op,onClick:ev=>{ev.stopPropagation();setOp(!op)},children:[(0,L.jsx)(`span`,{className:`pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),op?`Hide`:`Give worms`,(0,L.jsx)(`span`,{className:`wg-chev`,children:`⌄`})]}):null,give&&op?(0,L.jsx)(_WormGive,{id,kind}):null,!g?",
      'folded give row')
patch("tab===`worm`?(0,L.jsx)(_WormGivers,{kind:`p`,id})", "tab===`worm`?(0,L.jsx)(_WormGivers,{kind:`p`,id,give:1})", 'posts keep a (folded) give row')

# --- Bird ID: Flaps ---
FL = "[(0,L.jsx)(`span`,{className:`pp-ic bc-flap`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),`Flaps`,%s]"
patch("_clan?[_clan.e,`Clan`,_clan.n]:null,[`🪱`,`Worms`,_wc]]", "_clan?[_clan.e,`Clan`,_clan.n]:null," + FL % "_s.flaps||0" + ",[`🪱`,`Worms`,_wc]]", 'Bird card flaps')
patch("[_wc,_swc]=(0,_.useState)(0),", "[_wc,_swc]=(0,_.useState)(0),[_flc,_sflc]=(0,_.useState)(0),", 'nest flaps state')
patch("let{joined_at:j,worm_count:w}=await n.json();_swc(w||0);", "let{joined_at:j,worm_count:w,flaps:_f0}=await n.json();_swc(w||0);_sflc(_f0||0);", 'nest flaps load')
patch("_clanN?[_clanN.e,`Clan`,_clanN.n]:null,[`🪱`,`Worms`,_wc]]", "_clanN?[_clanN.e,`Clan`,_clanN.n]:null," + FL % "_flc" + ",[`🪱`,`Worms`,_wc]]", 'nest card flaps')

css = ("body .bc-e .bc-flap{display:inline-flex;color:#c084fc}body .bc-e .bc-flap .ri{width:19px;height:19px;display:block}"
       "body .wg-open{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 12px;margin:2px 0 10px;border-radius:999px;border:1px solid rgba(251,113,133,.35);background:rgba(251,113,133,.08);color:#fda4af;font:inherit;font-size:13px;font-weight:700;cursor:pointer}"
       "body .wg-open .ri.wemo{font-size:14px}body .wg-open .wg-chev{font-size:13px;line-height:1;transform:translateY(-3px);transition:transform .15s}body .wg-open.on .wg-chev{transform:rotate(180deg) translateY(-3px)}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
