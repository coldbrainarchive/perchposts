#!/usr/bin/env python3
"""Patch v1388 -> v1389: huddles use the post chat style — no huddle page any more.
- Opening a huddle goes straight into its chat (no ?chat=1 history step; back leaves).
- Header: members' birds + huddle name + "N birds"; tapping it grows the huddle panel down from the top
  (title, members row, Invite / Leave, mod tools), closed with the grab bar. No flaps/worms/share row.
- Filter row like posts: All chirps / Pinned / Top / Most replied / Media (no Flaps) + Oldest/Newest."""
import sys, re
src = '_deploy/assets/index-DUcNPOLc-v1388.js'
dst = '_deploy/assets/index-DUcNPOLc-v1389.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

# opening: huddles = posts
patch("let _openC=()=>{if(_cf)return;_cyR.current=window.scrollY;if(a||_nc||_sy||c&&!c.is_huddle){", "let _openC=()=>{if(_cf)return;_cyR.current=window.scrollY;if(a||_nc||_sy||c){", 'open no push')
patch("(0,_.useEffect)(()=>{if(c&&!c.is_huddle&&!_cf&&_cfR.current&&/^\\/post\\//.test(location.pathname))_setCF(!0)},[c,_cf]);",
      "(0,_.useEffect)(()=>{if(c&&!_cf&&_cfR.current&&/^\\/post\\//.test(location.pathname))_setCF(!0)},[c,_cf]);", 'keep in chat')
patch("if(window._cfWantPush){window._cfWantPush=!1;if(c.is_huddle){", "if(window._cfWantPush){window._cfWantPush=!1;if(!1){", 'no huddle push')
patch("if(a||_nc||_sy||_first&&(te.current||!c.is_huddle))_openC()}", "if(a||_nc||_sy||_first)_openC()}", 'always open')
patch("if(!c||!c.is_huddle&&!_cf)return(0,L.jsx)(_Bd,{});", "if(!c||!_cf)return(0,L.jsx)(_Bd,{});", 'loader until chat')
patch("window._ppRxHL=d;if(_cf&&c?.is_huddle)_closeC();", "window._ppRxHL=d;", 'rx no close')

# the huddle card goes into the panel like the post card
patch("_PBlk(c.is_huddle,_cf&&_chx?_chSlot:null,(0,L.jsxs)(`div`,{className:c.is_huddle?`content-card feed-post-card hp-card`:",
      "_PBlk(!1,_cf&&_chx?_chSlot:null,(0,L.jsxs)(`div`,{className:c.is_huddle?`content-card feed-post-card hp-card pp-pblk`:", 'portal huddle card')

# header
patch("flexWrap:_cf&&!c.is_huddle?`wrap`:void 0,rowGap:_cf&&!c.is_huddle?6:void 0,padding:_cf&&!c.is_huddle?`6px 12px 8px`:void 0",
      "flexWrap:_cf?`wrap`:void 0,rowGap:_cf?6:void 0,padding:_cf?`6px 12px 8px`:void 0", 'header layout')
patch("className:_cf?`cf-bar`+(c.is_huddle?``:` ch-bar`):void 0", "className:_cf?`cf-bar ch-bar`:void 0", 'ch-bar')
patch("\"aria-expanded\":_cf&&!c.is_huddle?_chx:void 0,onClick:_cf?(c.is_huddle?_closeC:()=>_setChx(v=>!v)):void 0",
      "\"aria-expanded\":_cf?_chx:void 0,onClick:_cf?()=>_setChx(v=>!v):void 0", 'header tap opens panel')
patch("flex:_cf&&!c.is_huddle?`1 1 100%`:void 0},children:[_cf&&!c.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`ch-back`",
      "flex:_cf?`1 1 100%`:void 0},children:[_cf&&(0,L.jsx)(`button`,{type:`button`,className:`ch-back`", 'row flex')
patch("_cf&&!c.is_huddle&&(0,L.jsx)(_ChThumb,{post:c},`cht`),_cf&&c.is_huddle&&(0,L.jsx)(`span`,{className:`cf-info`",
      "_cf&&(0,L.jsx)(_ChThumb,{post:c},`cht`),!1&&(0,L.jsx)(`span`,{className:`cf-info`", 'thumb')
patch("_cf&&!c.is_huddle?[(0,L.jsx)(_ChHeadTx,", "_cf?[(0,L.jsx)(_ChHeadTx,", 'head text')
patch("className:_cf&&!c.is_huddle?`ch-ctl`+(_chx?` off`:``):void 0,style:_cf&&!c.is_huddle?{",
      "className:_cf?`ch-ctl`+(_chx?` off`:``):void 0,style:_cf?{", 'controls row')
patch("_cf&&!c.is_huddle&&(0,L.jsx)(_ChFilter,{v:_cff,set:_setCff},`chf`)", "_cf&&(0,L.jsx)(_ChFilter,{v:_cff,set:_setCff,hud:!!c.is_huddle},`chf`)", 'filter')
patch("_cf&&!c.is_huddle&&_chx&&(0,L.jsx)(_ChXP,", "_cf&&_chx&&(0,L.jsx)(_ChXP,", 'panel')
patch("let _flt=!1;if(_cf&&!c?.is_huddle&&_cff!==`all`)", "let _flt=!1;if(_cf&&_cff!==`all`)", 'filtering')

# filter menu: no Flaps for huddles
patch("function _ChFilter({v,set}){", "function _ChFilter({v,set,hud}){", 'filter prop')
patch("Object.entries(_CHF).forEach(([k,l])=>{const b=document.createElement(`button`);",
      "Object.entries(_CHF).forEach(([k,l])=>{if(hud&&k===`react`)return;const b=document.createElement(`button`);", 'no flaps in huddles')

# panel bottom for huddles: only the grab bar
i = c.index("(0,L.jsx)(_ChDock,{...dock,chat:shut,grab:"); j = c.index("})]})}", i)
call = c[i:j+2]   # (0,L.jsx)(_ChDock,{...})
g = call[len("(0,L.jsx)(_ChDock,{...dock,chat:shut,grab:"):-2]
c = c[:i] + "dock.post.is_huddle?(0,L.jsx)(`div`,{className:`ch-dock ch-dock-h`,children:" + g + "}):" + call + c[j+2:]
print('OK huddle panel bottom')

# header picture + meta for huddles
patch("function _ChThumb({post}){const im=_chImg(post);", "function _ChThumb({post}){if(post.is_huddle)return(0,L.jsx)(_ChHudAv,{post});const im=_chImg(post);", 'huddle thumb')
patch("children:[site&&bot?(0,L.jsx)(`span`,{className:`s`,children:site}):post.username?",
      "children:[post.is_huddle?(0,L.jsx)(`span`,{children:(n=>`${n} bird${n===1?``:`s`}`)(_chHudM(post).length)}):site&&bot?(0,L.jsx)(`span`,{className:`s`,children:site}):post.username?", 'huddle meta')

patch("body .lb-ic{",
 "body .ch-th.ch-hx{position:relative;background:#1f222b;border-radius:50%!important;overflow:visible}"
 "body .ch-th.ch-hx .b{position:absolute;display:inline-flex;line-height:1}body .ch-th.ch-hx .b1{left:3px;top:4px;z-index:1}body .ch-th.ch-hx .b2{right:2px;bottom:3px;transform:scaleX(-1)}body .ch-th.ch-hx .solo{display:inline-flex}"
 "body .ch-th.ch-hx .hi{width:20px;height:20px;color:#94a3b8;display:inline-flex}body .ch-th.ch-hx .hi svg{width:100%;height:100%}"
 "body .chp.chp-full>.pp-pblk.hp-card{border:0!important;background:none!important;box-shadow:none!important;padding:0!important;margin:0!important}"
 "body .ch-dock.ch-dock-h{border-top:0;padding-top:4px}"
 "body .lb-ic{", 'css')

c += r"""
function _chHudM(p){try{const ms=JSON.parse(p.huddle_members||`[]`).map(x=>String(x).split(`:`)[0]).filter(Boolean);return[...new Set([p.username,...ms].filter(Boolean))]}catch(e){return p.username?[p.username]:[]}}
function _ChHudAv({post}){const me=(localStorage.getItem(`_myUsername`)||``).toLowerCase(),o=_chHudM(post).filter(n=>n.toLowerCase()!==me).slice(0,2);
 return(0,L.jsx)(`span`,{className:`ch-th ch-hx`,children:o.length===2?[(0,L.jsx)(`span`,{className:`b b1`,children:_ppFace(o[0],21)},`a`),(0,L.jsx)(`span`,{className:`b b2`,children:_ppFace(o[1],21)},`b`)]:o.length===1?(0,L.jsx)(`span`,{className:`solo`,children:_ppFace(o[0],28)}):(0,L.jsx)(`span`,{className:`hi`,dangerouslySetInnerHTML:{__html:_ppIco(`HUDDLE`)}})})}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
