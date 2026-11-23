#!/usr/bin/env python3
"""Patch v1319 -> v1320: New Post has one "+ TAG" chip instead of "+ REGION" and "+ FLOCK TAG".
It opens the searchable dropdown (spaces, regions, countries, flock tags; a new word -> "Use #word"). Picked country and
flock tag show as pills; tapping either removes it (fades out). The space pill still opens the picker (a post always
has a space). "+ TAG" hides once both a country and a flock tag are set. Search hint + an empty-state line about
making your own #tag."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1319.js'
dst = '_deploy/assets/index-DUcNPOLc-v1320.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("v&&!p&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>y(``),style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(kr,{country:v,small:!0})}),!v&&!p&&(0,L.jsx)(`button`,{type:`button`,className:`utag-add`,onClick:()=>x(e=>!e),children:`+ region`}),!p&&(0,L.jsx)(_UTagPick,{},`utp`)]})",
      "v&&!p&&(0,L.jsx)(`button`,{type:`button`,\"aria-label\":`Remove ${v}`,onClick:ev=>{const el=ev.currentTarget;el.classList.add(`np-out`);setTimeout(()=>y(``),170)},style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(kr,{country:v,small:!0})}),!p&&(0,L.jsx)(_UTagPick,{},`utp`),!p&&(0,L.jsx)(_NpAdd,{hasC:!!v,open:()=>x(e=>!e)},`npadd`)]})", 'chip row')
# _UTagPick: just the picked tag (tap removes); no own "+" chip or editor
old_pick_start = "function _UTagPick(){"
i = c.index(old_pick_start); j = c.index("function _UTagEdit(", i)
c = c[:i] + r"""function _UTagPick(){const[tag,setTag]=(0,_.useState)(``);(0,_.useEffect)(()=>{window._ppNewTag=null;const on=ev=>{const t=ev.detail;if(t){setTag(t);window._ppNewTag=t;dispatchEvent(new CustomEvent(`pp-np-tagset`))}};addEventListener(`pp-np-utag`,on);return()=>{window._ppNewTag=null;removeEventListener(`pp-np-utag`,on)}},[]);
 if(!tag)return null;return(0,L.jsx)(`button`,{type:`button`,"aria-label":`Remove #${tag}`,onClick:ev=>{const el=ev.currentTarget;el.classList.add(`np-out`);setTimeout(()=>{setTag(``);window._ppNewTag=null;dispatchEvent(new CustomEvent(`pp-np-tagset`))},170)},style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(_UTag,{tag,small:!0})})}
function _NpAdd({hasC,open}){const[,f]=(0,_.useState)(0);(0,_.useEffect)(()=>{const on=()=>f(x=>x+1);addEventListener(`pp-np-tagset`,on);return()=>removeEventListener(`pp-np-tagset`,on)},[]);
 if(hasC&&window._ppNewTag)return null;return(0,L.jsx)(`button`,{type:`button`,className:`utag-add`,onClick:open,children:`+ tag`})}
""" + c[j:]
print('OK: pick + add components')
patch("placeholder:`Search tags, regions, #tags`", "placeholder:`Search or make a #tag`", 'search hint')
patch("!k?cols:(0,L.jsx)(`div`,{className:`np-res`", "!k?[cols,(0,L.jsx)(`div`,{className:`np-hint`,children:[`Type a word to make your own `,(0,L.jsx)(_UTag,{tag:`tag`,small:!0})]},`hint`)]:(0,L.jsx)(`div`,{className:`np-res`", 'empty hint')
patch("body .lb-ic{", "@keyframes npOut{to{opacity:0;transform:scale(.7)}}body .np-out{animation:npOut .17s ease forwards;pointer-events:none}body .np-hint{display:flex;align-items:center;justify-content:center;gap:6px;padding:8px 12px 10px;border-top:1px solid #2a2d38;color:#64748b;font-size:12px;font-weight:600}body .lb-ic{", 'css')
patch("onClick:()=>{pickCountry(e.name);setQ(``)}", "onClick:()=>{pickCountry(e.name);setQ(``);close()}", 'close after country')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
