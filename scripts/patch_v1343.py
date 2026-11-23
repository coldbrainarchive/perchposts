#!/usr/bin/env python3
"""Patch v1342 -> v1343: search alerts.
- Saved searches Edit view: a bell next to the star turns alerts on/off for that search (purple bell = on); a small
  bell shows in the pill group when on.
- Alert notifications (icon SEARCH, from the worker): line search icon, "3 new posts" + the search's pills, preview of
  the newest match; tapping opens that search (e.link)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1342.js'
dst = '_deploy/assets/index-DUcNPOLc-v1343.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

# notifications
patch("if(!w||w==='You'||w==='Someone')return{kind:'system',col:'#c084fc',name:null,rest:tx,bird:null};",
      "if(e&&e.icon===`SEARCH`&&e.alert){const k=+e.an||1;return{kind:'system',col:'#c084fc',name:null,rest:[(0,L.jsx)(`span`,{children:`${k} new post${k===1?``:`s`} `},`a`),(0,L.jsx)(`span`,{className:`n-ss`,children:_ssPills(e.alert)},`p`)],bird:null}}"
      "if(!w||w==='You'||w==='Someone')return{kind:'system',col:'#c084fc',name:null,rest:tx,bird:null};", 'who')
patch(":(0,L.jsx)(`span`,{style:{fontSize:19,lineHeight:1},children:`🔔`});",
      ":e.icon===`SEARCH`?(0,L.jsx)(`span`,{className:`pp-ic n-srch`,dangerouslySetInnerHTML:{__html:_ppIco(`SEARCH`)}}):(0,L.jsx)(`span`,{style:{fontSize:19,lineHeight:1},children:`🔔`});", 'face')
patch("to:e.icon===`SHIELD`?`/mod?tab=flagged`:", "to:e.link?e.link:e.icon===`SHIELD`?`/mod?tab=flagged`:", 'link')

# saved searches: bell
patch("const star=qs=>_SS.set(_SS.load().map(x=>({...x,def:x.qs===qs?!x.def:!1})),!0),",
      "const star=qs=>_SS.set(_SS.load().map(x=>({...x,def:x.qs===qs?!x.def:!1})),!0),bell=qs=>_SS.set(_SS.load().map(x=>x.qs===qs?(x.alert?{qs:x.qs,def:x.def}:{...x,alert:!0}):x),!0),", 'bell fn')
patch("(0,L.jsxs)(`button`,{type:`button`,className:`ss-go`,onClick:ev=>{ev.stopPropagation();if(ed)return;go(x.qs)},children:[!ed&&x.def?(0,L.jsx)(`span`,{className:`ss-defic`,title:`Default`,dangerouslySetInnerHTML:{__html:_SS_IC.starOn}},`d`):null,..._ssPills(x.qs)]}),",
      "ed?(0,L.jsx)(`button`,{type:`button`,className:`ss-bell`+(x.alert?` on`:``),\"aria-label\":x.alert?`Turn off alerts`:`Alert me about new posts`,onClick:ev=>{ev.stopPropagation();bell(x.qs)},dangerouslySetInnerHTML:{__html:x.alert?_SS_IC.bellOn:_SS_IC.bell}}):null,"
      "(0,L.jsxs)(`button`,{type:`button`,className:`ss-go`,onClick:ev=>{ev.stopPropagation();if(ed)return;go(x.qs)},children:[!ed&&x.def?(0,L.jsx)(`span`,{className:`ss-defic`,title:`Default`,dangerouslySetInnerHTML:{__html:_SS_IC.starOn}},`d`):null,!ed&&x.alert?(0,L.jsx)(`span`,{className:`ss-belic`,title:`Alerts on`,dangerouslySetInnerHTML:{__html:_SS_IC.bellOn}},`bl`):null,..._ssPills(x.qs)]}),", 'bell button')
patch("ed?(0,L.jsx)(`div`,{className:`ss-none`,children:`Star one to fill your search bar when you open Perch Posts.`}):null",
      "ed?(0,L.jsxs)(`div`,{className:`ss-none`,children:[(0,L.jsx)(`div`,{children:`Star: fills your search bar when you open Perch Posts.`}),(0,L.jsx)(`div`,{children:`Bell: get a notification when new posts match.`})]}):null", 'hint')
patch("x:`<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.4\" stroke-linecap=\"round\"><path d=\"M6 6l12 12M18 6 6 18\"/></svg>`};",
      "x:`<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.4\" stroke-linecap=\"round\"><path d=\"M6 6l12 12M18 6 6 18\"/></svg>`,"
      "bell:`<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z\"/><path d=\"M10 20.5a2.2 2.2 0 0 0 4 0\"/></svg>`,"
      "bellOn:`<svg viewBox=\"0 0 24 24\" fill=\"currentColor\" stroke=\"currentColor\" stroke-width=\"2.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z\"/><path d=\"M10 20.5a2.2 2.2 0 0 0 4 0\" fill=\"none\"/></svg>`};", 'icons')
patch("body .lb-ic{",
 "body .ss-bell{flex-shrink:0;display:inline-flex;width:26px;height:26px;align-items:center;justify-content:center;border:0;background:none;padding:0;color:#475569;cursor:pointer}"
 "body .ss-bell svg,body .ss-belic svg{width:16px;height:16px}body .ss-bell.on,body .ss-belic{color:#c084fc}body .ss-belic{display:inline-flex;margin-right:1px}"
 "body .n-ss{display:inline-flex;flex-wrap:wrap;gap:4px;vertical-align:middle;margin:2px 0}body .n-ss>*{transform:scale(.9);transform-origin:left center}"
 "body .n-srch{display:inline-flex;color:#c084fc}body .n-srch svg{width:19px;height:19px}"
 "body .lb-ic{", 'css')
patch("function _nPrev(e){return e&&e.req&&e.preview?", "function _nPrev(e){return e&&(e.req||e.alert)&&e.preview?", 'alert preview')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
