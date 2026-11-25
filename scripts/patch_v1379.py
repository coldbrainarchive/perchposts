#!/usr/bin/env python3
"""Patch v1378 -> v1379 (PREVIEW): post chat header gets the scroller's action row.
- Under the post title: flaps | worms (bird posts only) | share, styled like the scroller panel row, usable without opening.
- Tapping the header still opens the full post; the action row moves to the bottom of the opened post
  (the post card's own pills are hidden there so they aren't doubled). A grab handle sits under the row.
- Huddles unchanged."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1378.js'
dst = '_deploy/assets/index-DUcNPOLc-v1379.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

FLAP = "async t=>{if(c.frozen)return;if(!e){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}t.preventDefault();if(_ppOwn(c.username)){_ppOwnMsg();return}const _nv=re.myVote===1?0:1;const _os=_nv?re.score+1:Math.max(0,re.score-1);ie({score:_os,myVote:_nv});_lastVoteTs=Date.now();let n=await Tr(c.id,_nv);if(n.success)ie({score:n.score,myVote:n.myVote})}"
DOCK = "(0,L.jsx)(_ChDock,{post:c,score:re.score,mine:re.myVote===1,open:_chx,toggle:()=>_setChx(v=>!v),onFlap:" + FLAP + "},`chdk`)"

# collapsed: the row sits between the title row and the filter/sort row
patch("(0,L.jsxs)(`div`,{className:_cf&&!c.is_huddle?`ch-ctl`+(_chx?` off`:``):void 0,",
      "_cf&&!c.is_huddle&&!_chx&&" + DOCK + ",(0,L.jsxs)(`div`,{className:_cf&&!c.is_huddle?`ch-ctl`+(_chx?` off`:``):void 0,", 'dock collapsed')
# opened: the row sits at the bottom of the opened post
patch("_cf&&!c.is_huddle&&_chx&&(0,L.jsx)(`div`,{className:`chp chp-full`,ref:_setChSlot},`chp`),",
      "_cf&&!c.is_huddle&&_chx&&(0,L.jsx)(`div`,{className:`chp chp-full`,ref:_setChSlot},`chp`),_cf&&!c.is_huddle&&_chx&&(0,L.jsx)(`div`,{className:`ch-dockx`,children:" + DOCK + "},`chdkx`),", 'dock opened')

CSS = ("body .ch-dock{flex:1 1 100%;display:flex;flex-direction:column;margin:2px -12px -8px;border-top:1px solid #23262e}"
 "body .ch-dock-row{display:flex;align-items:stretch;height:40px}"
 "body .ch-db{flex:1;position:relative;display:flex;align-items:center;justify-content:center;gap:6px;border:0;background:none;color:#cbd5e1;font:inherit;font-size:13px;font-weight:800;letter-spacing:.02em;cursor:pointer;padding:0;-webkit-tap-highlight-color:transparent;-webkit-touch-callout:none;-webkit-user-select:none;user-select:none}"
 "body .ch-db+.ch-db::before{content:'';position:absolute;left:0;top:11px;bottom:11px;width:1.5px;background:rgba(148,163,184,.35)}"
 "body .ch-db:active{background:rgba(148,163,184,.12)}"
 "body .ch-db.on{color:#c084fc}"
 "body .ch-db .pp-ic .ri{width:17px;height:17px;stroke-width:2.1}body .ch-db.ch-fl .pp-ic .ri{width:19px;height:19px}body .ch-db.ch-sh .pp-ic .ri{width:11px;height:11px}"
 "body .ch-grab{display:flex;justify-content:center;padding:0 0 7px;cursor:pointer}body .ch-grab i{width:36px;height:4px;border-radius:2px;background:#3a3e4a}"
 "body .ch-dockx{flex-shrink:0;background:#15171d;padding:0 12px 8px}body .ch-dockx .ch-dock{margin:0 -12px -8px}"
 "body .chp.chp-full>.pp-pblk .feed-post-actions{display:none!important}"
 "body .lb-ic{")
patch("body .lb-ic{", CSS, 'css')

c += r"""
function _ChDock({post:c,score,mine,open,toggle,onFlap}){const[,f]=(0,_.useState)(0);
 const hu=!!c.username&&!_ppIsBot(c)&&!/^Anon #/.test(c.username),K=_ppWorm.key(`p`,c.id);
 (0,_.useEffect)(()=>{if(!hu)return;_ppWorm.want(`p`,c.id);return _ppWorm.sub(K,()=>f(x=>x+1))},[K,hu]);
 (0,_.useEffect)(()=>{const h=ev=>{ev.detail&&ev.detail.id===c.id&&f(x=>x+1)};addEventListener(`pp-sharen`,h);return()=>removeEventListener(`pp-sharen`,h)},[c.id]);
 const[said,setSaid]=(0,_.useState)(``);const shn=_ppShN(c.id,c.share_count);
 const share=async ev=>{ev.stopPropagation();if(window._ppShare&&window._ppShare(c.id))return;const u=`${location.origin}/post/${c.id}`;let ok=!1;try{if(navigator.share){await navigator.share({url:u});ok=!0}else if(navigator.clipboard&&navigator.clipboard.writeText){await navigator.clipboard.writeText(u);ok=!0}}catch(er){}if(ok){setSaid(`Shared`);setTimeout(()=>setSaid(``),1800)}};
 const worm=ev=>{ev.stopPropagation();if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}const me=(localStorage.getItem(`_myUsername`)||``).toLowerCase();_wormWallet(c.id,!!me&&me===c.username.toLowerCase(),1)};
 const flap=ev=>{ev.stopPropagation();const b=ev.currentTarget;if(!mine&&localStorage.getItem(`auth_token`)&&!_ppOwn(c.username))_ppFlapAnim(b);onFlap(ev)};
 return(0,L.jsxs)(`div`,{className:`ch-dock`,onClick:ev=>ev.stopPropagation(),children:[(0,L.jsxs)(`div`,{className:`ch-dock-row`,children:[
  (0,L.jsxs)(`button`,{type:`button`,className:`ch-db ch-fl`+(mine?` on`:``),"aria-label":`Flap`,onClick:flap,children:[(0,L.jsx)(`span`,{className:`pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),(0,L.jsx)(`span`,{children:score})]}),
  hu?(0,L.jsxs)(`button`,{type:`button`,className:`ch-db ch-wm`+(_ppWorm.m(K)?` on`:``),"aria-label":`Worms`,onClick:worm,children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`,"data-wk":K,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{children:_ppWorm.n(K)||0})]}):null,
  (0,L.jsxs)(`button`,{type:`button`,className:`ch-db ch-sh`+(said?` on`:``),"aria-label":`Share`,onClick:share,children:[(0,L.jsx)(`span`,{className:`pp-ic pp-share`,dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),(0,L.jsx)(`span`,{children:said||(shn>0?shn:`Share`)})]})]}),
  (0,L.jsx)(`div`,{className:`ch-grab`,role:`button`,"aria-label":open?`Close the post`:`Open the post`,onClick:ev=>{ev.stopPropagation();toggle()},children:(0,L.jsx)(`i`,{})})]})}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
