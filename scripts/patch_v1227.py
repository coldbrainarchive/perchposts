#!/usr/bin/env python3
"""Patch v1226 -> v1227: new posts wait for you.
The home feed reloads every 30 s. If you're scrolled down (or in the post scroller) and new posts have
arrived, the feed no longer changes under you: a "↑ N NEW POSTS" pill shows at the top instead. Tap it
to load them and jump to the top (in the scroller it closes the scroller first). Scrolling back to the
top yourself loads them too. At the top of the feed new posts just appear as before."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1226.js'
dst = '_deploy/assets/index-DUcNPOLc-v1227.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# 1. The feed refresh hands its new list to _ppNewHold instead of swapping it in straight away
patch("_hmR.current=_gj.next_before??null;r(", "const _nb=_gj.next_before??null;r(", 'keep the older-posts cursor with the list')
patch("t(o),a(x=>({...x,..._vv}));_fseen.clear()},[])",
      "a(x=>({...x,..._vv}));_ppNewHold(t,o,()=>{_hmR.current=_nb;_fseen.clear()})},[])", 'hold new posts while scrolled')

# 2. The helper and the pill
JS = r"""
var _ppNP={apply:null,el:null};
function _ppHeld(){try{return window.scrollY>400||!!document.querySelector(`.reel`)}catch(e){return!1}}
function _ppNewHold(set,list,after){
  set(prev=>{
    if(!prev||!prev.length||!_ppHeld()){_ppNP.apply=null;_ppPill(0);after();return list}
    const ids=new Set(prev.map(x=>x.id)),n=list.filter(x=>!ids.has(x.id)).length;
    if(!n){after();return list}
    _ppNP.apply=()=>{_ppNP.apply=null;_ppPill(0);set(list);after()};
    _ppPill(n);return prev})}
function _ppPillGo(){const go=_ppNP.apply;if(!go)return;_ppPill(0);
  // Close the scroller first (it puts the page back where it was), then load the new posts and go to the top
  const x=document.querySelector(`.reel .reel-x`);if(x)x.click();
  const top=()=>window.scrollTo(0,0);
  setTimeout(()=>{go();requestAnimationFrame(()=>{top();setTimeout(top,120);setTimeout(top,400)})},x?320:0)}
function _ppPill(n){
  let el=_ppNP.el;
  if(!n){if(el)el.classList.remove(`on`);return}
  if(!el){el=_ppNP.el=document.createElement(`button`);el.type=`button`;el.className=`pp-newpill`;
    el.addEventListener(`click`,e=>{e.stopPropagation();_ppPillGo()});document.body.appendChild(el);
    window.addEventListener(`scroll`,()=>{if(_ppNP.apply&&window.scrollY<80&&!document.querySelector(`.reel`))_ppNP.apply()},{passive:!0})}
  // Sit just under the sticky header and search bar
  let y=0;try{const tb=document.querySelector(`.app-topbar`);if(tb)y=Math.max(y,tb.getBoundingClientRect().bottom);
    const si=document.querySelector(`input[placeholder^="Search"]`),sb=si&&si.parentElement&&si.parentElement.getBoundingClientRect();
    if(sb&&sb.top>=0&&sb.bottom<220)y=Math.max(y,sb.bottom)}catch(e){}
  el.style.setProperty(`--pp-np-top`,(y+10)+`px`);
  try{const rx=document.querySelector(`.reel .reel-x`);if(rx)el.style.setProperty(`--pp-np-reel`,rx.getBoundingClientRect().top+`px`)}catch(e){}
  el.innerHTML=`<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5.5 11.5 12 5l6.5 6.5"/></svg><span>${n} new post${n===1?``:`s`}</span>`;
  requestAnimationFrame(()=>el.classList.add(`on`))}
"""
patch("function _reelOpen(card,o){", JS + "function _reelOpen(card,o){", 'helper')

CSS = ("body .pp-newpill{position:fixed;left:50%;top:var(--pp-np-top,120px);z-index:60;display:inline-flex;align-items:center;gap:6px;"
       "height:36px;padding:0 16px;border:0;border-radius:999px;background:#c084fc;color:#14161c;font-family:inherit;font-weight:800;font-size:13px;line-height:1;letter-spacing:.06em;"
       "text-transform:uppercase;box-shadow:0 6px 20px rgba(0,0,0,.45);cursor:pointer;-webkit-tap-highlight-color:transparent;"
       "opacity:0;pointer-events:none;transform:translate(-50%,-14px);transition:opacity .2s,transform .2s}"
       "body .pp-newpill.on{opacity:1;pointer-events:auto;transform:translate(-50%,0)}"
       "body:has(.reel) .pp-newpill{top:var(--pp-np-reel,calc(22px + env(safe-area-inset-top)));height:38px;z-index:9600}"
       "body:has(.pp-newpill.on) .reel .reel-hint{opacity:0!important}")
patch("body .lb-ic{", CSS + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
