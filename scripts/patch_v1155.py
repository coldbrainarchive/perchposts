#!/usr/bin/env python3
"""Patch v1154 -> v1155:
- Tapping a 🪱 pill (feed card or post page) opens the Worm wallet with the post's Flaps view open underneath.
- The Flaps view's All / Flaps / 🪱 tabs become one filter button ("All ▾") with a small menu: All · Flaps · Worms.
  Shown only when the post has both flaps and worms."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1154.js'
dst = '_deploy/assets/index-DUcNPOLc-v1155.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# filter menu helper
patch("function _wwPanel({kind,id,own,done}){",
      r'''function _prFilterMenu(btn,cur,opts,set){const ex=document.querySelector(`.cp-menu`);if(ex){ex._close?ex._close():ex.remove();return}
 const m=document.createElement(`div`);m.className=`cp-menu`;m.setAttribute(`role`,`menu`);
 opts.forEach(([k,ico,lb])=>{const b=document.createElement(`button`);b.type=`button`;b.className=`cp-opt`+(k===cur?` on`:``);b.dataset.k=k;b.innerHTML=(ico?`<span class="pp-ic lb-ic">${_ppIco(ico)}</span>`:``);b.append(lb);b.onclick=e=>{e.stopPropagation();set(k);close()};m.append(b)});
 document.body.append(m);const r=btn.getBoundingClientRect();m.style.left=Math.max(8,Math.min(r.left,innerWidth-m.offsetWidth-8))+`px`;
 m.style.top=(r.bottom+6+m.offsetHeight>innerHeight-8&&r.top-6-m.offsetHeight>8?r.top-6-m.offsetHeight:r.bottom+6)+`px`;requestAnimationFrame(()=>m.classList.add(`in`));
 const out=e=>{if(!m.contains(e.target)&&e.target!==btn)close()};const close=()=>{m.remove();document.removeEventListener(`pointerdown`,out,!0);removeEventListener(`scroll`,close,!0)};m._close=close;
 setTimeout(()=>{document.addEventListener(`pointerdown`,out,!0);addEventListener(`scroll`,close,!0)},0)}
function _wwPanel({kind,id,own,done}){''', 'filter menu')
# tabs → one filter button
patch("(0,L.jsxs)(`div`,{className:`pr-tabs`+(_two?``:` pr-notabs`),children:[..._two?[T(`all`,`All ${list.length}`),T(`flap`,[ic(`BIRD`),nf]),T(`worm`,[ic(`WORM`),nw])]:[]]}),",
      "_two?(0,L.jsx)(`div`,{className:`pr-tabs pr-filter-row`,children:(0,L.jsxs)(`button`,{type:`button`,className:`cp-filter pr-filter`,\"data-k\":_tb2,onClick:ev=>{ev.stopPropagation();_prFilterMenu(ev.currentTarget,_tb2,[[`all`,null,`All`],[`flap`,`BIRD`,`Flaps`],[`worm`,`WORM`,`Worms`]],setTab)},children:[_tb2===`flap`?ic(`BIRD`):_tb2===`worm`?ic(`WORM`):null,_tb2===`flap`?`Flaps`:_tb2===`worm`?`Worms`:`All`,(0,L.jsx)(`span`,{className:`cp-caret`,children:`▾`})]})}):null,",
      'filter button')
# the worm filter shows worm rows (same rows as All), the flap filter flap rows
patch(" const show=_tb2===`all`?list.flatMap(p=>[p.flap?[p,`f`]:null,p.worms?[p,`w`]:null].filter(Boolean)):list.filter(p=>p.flap).map(p=>[p,`f`]);",
      " const show=_tb2===`all`?list.flatMap(p=>[p.flap?[p,`f`]:null,p.worms?[p,`w`]:null].filter(Boolean)):_tb2===`worm`?list.filter(p=>p.worms>0).map(p=>[p,`w`]):list.filter(p=>p.flap).map(p=>[p,`f`]);", 'worm filter rows')
patch("_tb2===`worm`&&!bot?(0,L.jsx)(_WormGivers,{kind:`p`,id}):!ppl?", "!ppl?", 'worm filter uses the rows')
# post page 🪱 pill: wallet + Flaps underneath; and when arriving from a card's 🪱
patch("if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}_wormWallet(id,own)},children:[",
      "if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}if(pv)setCpm(`react`);_wormWallet(id,own)},children:[", 'post pill: Flaps underneath')
patch("function _PostRespLine({id,pv,setCpm,own}){const ppl=_usePrx(id),[open,setOpen]=(0,_.useState)(!1);(0,_.useEffect)(()=>{_ppWorm.want(`p`,id)},[id]);",
      "const _ppWalletNext=new Set();\nfunction _PostRespLine({id,pv,setCpm,own}){const ppl=_usePrx(id),[open,setOpen]=(0,_.useState)(!1);(0,_.useEffect)(()=>{_ppWorm.want(`p`,id);if(_ppWalletNext.delete(id)&&localStorage.getItem(`auth_token`))setTimeout(()=>_wormWallet(id,own),700)},[id]);", 'arrival opens the wallet')
patch("onClick:ev=>{ev.stopPropagation();_ppRxOpen.add(id)},children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`",
      "onClick:ev=>{ev.stopPropagation();_ppRxOpen.add(id);_ppWalletNext.add(id)},children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`", 'card 🪱 opens the wallet')
patch("body .lb-ic{", "body .pr-filter-row{justify-content:flex-start;margin-bottom:10px}body .pr-filter{display:inline-flex;align-items:center;gap:6px}body .pr-filter .pr-ic svg.ri{width:18px!important;height:18px!important;stroke-width:2.6}body .cp-opt[data-k=flap] .lb-ic{color:#c084fc}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
