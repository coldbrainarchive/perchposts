#!/usr/bin/env python3
"""Patch v1355 -> v1356: the post page goes away — a post IS its chat (huddles unchanged).
- Opening any post goes straight to the chat (no history step back to a post page). A ‹ back button leaves.
- The ▾ drop-down under the header now holds the real post: tags, text, photos/link, flaps/worms/share,
  edit/delete, mod tools (it replaces the small summary panel from v1355).
- Flaps notifications open the chat with the Flaps filter on; "tagged you in a post" opens it with the drop-down open."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1355.js'
dst = '_deploy/assets/index-DUcNPOLc-v1356.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch("[_chx,_setChx]=(0,_.useState)(!1),", "[_chx,_setChx]=(0,_.useState)(!1),[_chSlot,_setChSlot]=(0,_.useState)(null),", 'slot state')

# posts: the whole post card is portalled into the chat drop-down (only while open); huddles keep it in place
patch("(0,L.jsxs)(`div`,{className:c.is_huddle?`content-card feed-post-card hp-card`:`content-card feed-post-card`,",
      "_PBlk(c.is_huddle,_cf&&_chx?_chSlot:null,(0,L.jsxs)(`div`,{className:c.is_huddle?`content-card feed-post-card hp-card`:`content-card feed-post-card pp-pblk`,", 'wrap open')
patch("]}),(0,L.jsx)(`section`,{className:`comments-shell`+",
      "]})),(0,L.jsx)(`section`,{className:`comments-shell`+", 'wrap close')

# the drop-down is now a slot the post block portals into
patch("_cf&&!c.is_huddle&&_chx&&(0,L.jsx)(_ChPanel,{post:c,close:()=>_setChx(!1),openPost:()=>{_setChx(!1);_closeC()}},`chp`)",
      "_cf&&!c.is_huddle&&_chx&&(0,L.jsx)(`div`,{className:`chp chp-full`,ref:_setChSlot},`chp`)", 'slot')

# back button (posts) at the left of the header
patch("children:[_cf&&!c.is_huddle&&(0,L.jsx)(_ChThumb,{post:c},`cht`),",
      "children:[_cf&&!c.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`ch-back`,\"aria-label\":`Back`,onClick:ev=>{ev.stopPropagation();(history.state&&history.state.idx>0)?history.back():o(`/`)},dangerouslySetInnerHTML:{__html:`<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.4\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15 5l-7 7 7 7\"/></svg>`}},`chb`),_cf&&!c.is_huddle&&(0,L.jsx)(_ChThumb,{post:c},`cht`),", 'back button')

# opening: posts never push a history step for the chat
patch("let _openC=()=>{if(_cf)return;_cyR.current=window.scrollY;if(a||_nc||_sy){",
      "let _openC=()=>{if(_cf)return;_cyR.current=window.scrollY;if(a||_nc||_sy||c&&!c.is_huddle){", 'openC no push for posts')
patch("else{history.replaceState(history.state,``,location.pathname);history.pushState(history.state,``,location.pathname+`?chat=1`);window._cfPushed=!0}_cyR.current=0;O.current=!0;_setCF(!0)},[]);",
      "else{window._cfWantPush=!0;window._cfPushed=!1;history.replaceState(history.state,``,location.pathname+`?chat=1`)}_cyR.current=0;O.current=!0;_setCF(!0)},[]);", 'chat=1 load: decide push later')
patch("(0,_.useEffect)(()=>{if(!c)return;let _k=[r,a,_nc,_sy].join(`|`);",
      "(0,_.useEffect)(()=>{if(c&&!c.is_huddle&&!_cf&&_cfR.current&&/^\\/post\\//.test(location.pathname))_setCF(!0)},[c,_cf]);(0,_.useEffect)(()=>{if(!c)return;if(window._cfWantPush){window._cfWantPush=!1;if(c.is_huddle){history.replaceState(history.state,``,location.pathname);history.pushState(history.state,``,location.pathname+`?chat=1`);window._cfPushed=!0}}let _k=[r,a,_nc,_sy].join(`|`);", 'huddle push after load + keep posts in chat')
patch("if(a||_nc||_sy||_first&&te.current)_openC()},[c,a,_nc,_sy]);",
      "if(a||_nc||_sy||_first&&(te.current||!c.is_huddle))_openC()},[c,a,_nc,_sy]);", 'posts always open chat')

# flaps notifications -> Flaps filter; tagged-in-post -> drop-down open
patch("_setCpm((_ppRxOpen.delete(r)||_rk)?(",
      "_setCff(`all`);_setChx(_rq.get(`pd`)===`1`);_setCpm((_ppRxOpen.delete(r)||_rk)?(_setCff(`react`),", 'rx -> flaps filter')
patch("window._ppRxHL=d;if(_cf)_closeC();_setCpm(`react`);",
      "window._ppRxHL=d;if(_cf&&c?.is_huddle)_closeC();_setCff(`react`);_setCpm(`react`);", 'pp-rx event')
patch("if(e.icon===`AT`&&!e.targetId)return '';", "if(e.icon===`AT`&&!e.targetId)return `?pd=1`;", 'tag notif opens drop-down')

patch("body .lb-ic{",
 "body .ch-back{width:34px;height:34px;flex-shrink:0;border:0;background:none;color:#e2e8f0;display:inline-flex;align-items:center;justify-content:center;padding:0;margin-left:-6px;cursor:pointer;border-radius:999px}"
 "body .ch-back svg{width:22px;height:22px}"
 "body .ch-bar{gap:6px!important}body .ch-bar .ch-th{width:34px;height:34px}"
 "body .ch-m>span{flex-shrink:0}body .ch-m>span:first-child{flex-shrink:1;min-width:0;overflow:hidden;text-overflow:ellipsis}"
 "body .chp.chp-full{margin:0;border:0;border-radius:0;border-bottom:1px solid #22252e;background:#15171d;padding:12px 14px 6px;display:block;max-height:68vh;box-shadow:none;overscroll-behavior:contain}"
 "body .chp.chp-full>.pp-pblk{margin:0!important;border:0;border-radius:0;background:none;box-shadow:none;padding:0 0 4px}"
 "body .lb-ic{", 'css')

c += r"""
function _PBlk(h,slot,el){if(h)return el;if(!slot)return null;return m().createPortal(el,slot)}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
