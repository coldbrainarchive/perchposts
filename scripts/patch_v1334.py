#!/usr/bin/env python3
"""Patch v1333 -> v1334: popular flock tags show instantly in the Tags dropdown.
Fetched once soon after page load (and remembered from the last visit in localStorage), so the
dropdown renders them straight away; refreshed quietly in the background each time it opens.
If nothing is ready yet they fade in instead of popping."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1333.js'
dst = '_deploy/assets/index-DUcNPOLc-v1334.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch("function _UTagPopular({pick}){const[tags,setTags]=(0,_.useState)(null);(0,_.useEffect)(()=>{fetch(`${R}/tags?popular=1`).then(r=>r.ok?r.json():{tags:[]}).then(d=>setTags(d.tags||[])).catch(()=>setTags([]))},[]);\n if(!tags||!tags.length)return null;return(0,L.jsxs)(`div`,{className:`utag-pop`,",
"""function _ppPopLoad(){if(window._ppPopP)return window._ppPopP;window._ppPopP=fetch(`${R}/tags?popular=1`).then(r=>r.ok?r.json():null).then(d=>{if(d&&Array.isArray(d.tags)){window._ppPopTags=d.tags;try{localStorage.setItem(`pp_pop_tags`,JSON.stringify(d.tags))}catch(e){}}return window._ppPopTags||[]}).catch(()=>window._ppPopTags||[]).finally(()=>{setTimeout(()=>{window._ppPopP=null},60000)});return window._ppPopP}
try{if(!window._ppPopTags){const s=JSON.parse(localStorage.getItem(`pp_pop_tags`)||`null`);if(Array.isArray(s))window._ppPopTags=s}}catch(e){}
setTimeout(()=>{try{_ppPopLoad()}catch(e){}},1200);
function _UTagPopular({pick}){const[tags,setTags]=(0,_.useState)(()=>window._ppPopTags||null);const fade=(0,_.useRef)(!window._ppPopTags);(0,_.useEffect)(()=>{let dead=!1;_ppPopLoad().then(t=>{dead||setTags(t)});return()=>{dead=!0}},[]);
 if(!tags||!tags.length)return null;return(0,L.jsxs)(`div`,{className:`utag-pop`+(fade.current?` utag-pop-in`:``),""", 'component')

patch("body .lb-ic{", "@keyframes utagPopIn{from{opacity:0}to{opacity:1}}.utag-pop-in{animation:utagPopIn .22s ease-out}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
