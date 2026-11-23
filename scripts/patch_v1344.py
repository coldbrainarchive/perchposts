#!/usr/bin/env python3
"""Patch v1343 -> v1344:
1. Typing in the search bar shows your saved searches that contain the word (perch tag, region/country, flock tag,
   bird or keyword) at the top of the results; tap fills the bar.
2. Tapping the bookmark opens the dropdown (Tags tab) and briefly highlights the search you just saved."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1343.js'
dst = '_deploy/assets/index-DUcNPOLc-v1344.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch(":(0,L.jsxs)(L.Fragment,{children:[(C||P||w)&&(0,L.jsxs)(`div`,{className:`search-columns`",
      ":(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(_SavedMatch,{q:n,go:_goSaved},`ssm`),(C||P||w)&&(0,L.jsxs)(`div`,{className:`search-columns`", 'results')
patch("(0,L.jsx)(_SaveSearchBtn,{params:e,kw:n},`ssb`)",
      "(0,L.jsx)(_SaveSearchBtn,{params:e,kw:n,onSaved:qs=>{window._ssHL={qs,t:Date.now()};_pickTab(`boards`);a(!0)}},`ssb`)", 'bar button props')
patch("function _SaveSearchBtn({params,kw}){", "function _SaveSearchBtn({params,kw,onSaved}){", 'btn sig')
patch("_SS.set([...cur,{qs:key,def:!1}],!0);setPop(!0);setTimeout(()=>setPop(!1),360)},",
      "_SS.set([...cur,{qs:key,def:!1}],!0);setPop(!0);setTimeout(()=>setPop(!1),360);onSaved&&onSaved(key)},", 'btn onSaved')
patch("(0,L.jsxs)(`div`,{className:`ss-it`,children:[",
      "(0,L.jsxs)(`div`,{className:`ss-it`+(_ssHot(x.qs)?` ss-hl`:``),children:[", 'highlight row')
patch("body .lb-ic{",
 "@keyframes ssHl{0%,35%{box-shadow:0 0 0 2px #c084fc,0 0 16px rgba(192,132,252,.55)}100%{box-shadow:0 0 0 0 rgba(192,132,252,0)}}"
 "body .ss-hl .ss-go{animation:ssHl 1.8s ease-out}"
 "body .ss-m{padding:6px 14px 8px;border-bottom:1px solid #2a2d38;margin-bottom:4px}body .ss-m .search-section-label{text-align:left!important;padding:0 0 2px 40px!important;margin:0!important;line-height:26px}"
 "body .lb-ic{", 'css')

c += r"""
function _ssHot(qs){const h=window._ssHL;return!!h&&h.qs===qs&&Date.now()-h.t<2500}
function _ssText(qs){const p=new URLSearchParams(qs),out=[];for(const[k,v]of p){if(k===`flock`){out.push(`flock`);continue}if(k===`board`){const o=nr.find(e=>e.slug===v);out.push(v,o?o.name:``);continue}if(k===`bot`){out.push(v===`hide`?`no bots`:`bots`);continue}out.push(v)}return out.join(` `).toLowerCase()}
function _SavedMatch({q,go}){const list=_ssUse();if(!localStorage.getItem(`auth_token`))return null;const k=String(q||``).trim().toLowerCase().replace(/^#+/,``);if(k.length<2)return null;
 const m=list.filter(x=>_ssText(x.qs).includes(k));if(!m.length)return null;
 return(0,L.jsxs)(`div`,{className:`ss-m`,onMouseDown:ev=>ev.preventDefault(),children:[(0,L.jsx)(`div`,{className:`search-section-label`,children:`Saved searches`}),(0,L.jsx)(`div`,{className:`ss-list`,children:m.map(x=>(0,L.jsx)(`div`,{className:`ss-it`+(_ssHot(x.qs)?` ss-hl`:``),children:(0,L.jsxs)(`button`,{type:`button`,className:`ss-go`,onClick:ev=>{ev.stopPropagation();go(x.qs)},children:[x.def?(0,L.jsx)(`span`,{className:`ss-defic`,dangerouslySetInnerHTML:{__html:_SS_IC.starOn}},`d`):null,x.alert?(0,L.jsx)(`span`,{className:`ss-belic`,dangerouslySetInnerHTML:{__html:_SS_IC.bellOn}},`bl`):null,..._ssPills(x.qs)]})},x.qs))})]})}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
