#!/usr/bin/env python3
"""Patch v1321 -> v1322: every post needs at least one tag.
- New Post starts with no perch tag (unless opened from a perch tag's page, or caged). The row is just "+ TAG".
- Posting with no perch tag and no flock tag: "+ TAG" glows and says "Add a tag"; nothing posts.
- Only a flock tag: sent with board_auto (worker files it under Random); cards, the post page, the scroller and share
  cards don't show that Random pill."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1321.js'
dst = '_deploy/assets/index-DUcNPOLc-v1322.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# start empty
patch("(sr(i.get(`board`))?.slug)||`random`),[v,y]", "(sr(i.get(`board`))?.slug)||``),[v,y]", 'no default perch tag')
patch("oe=sr(h)||nr[0];", "oe=sr(h)||null;", 'oe may be empty')
patch("(0,L.jsx)(`button`,{type:`button`,onClick:()=>{p||(x(e=>!e),C(null))},style:{background:`none`,border:`none`,padding:0,cursor:p?`default`:`pointer`},children:(0,L.jsx)(Ar,{boardName:oe.name,small:!0})}),",
      "oe&&(0,L.jsx)(`button`,{type:`button`,onClick:()=>{p||(x(e=>!e),C(null))},style:{background:`none`,border:`none`,padding:0,cursor:p?`default`:`pointer`},children:(0,L.jsx)(Ar,{boardName:oe.name,small:!0})}),", 'space pill only when picked')
patch("!p&&(0,L.jsx)(_NpAdd,{hasC:!!v,open:()=>x(e=>!e)},`npadd`)", "!p&&(0,L.jsx)(_NpAdd,{hasC:!!v,hasP:!!h,open:()=>x(e=>!e)},`npadd`)", 'add chip knows perch tag')
# submit check + auto board
patch("if(_isHuddle&&_hmTagged.length===0)return alert(`Add at least one user to your huddle`);",
      "if(_isHuddle&&_hmTagged.length===0)return alert(`Add at least one user to your huddle`);if(!_isHuddle&&!p&&!h&&!window._ppNewTag){dispatchEvent(new CustomEvent(`pp-np-need`));return}", 'require a tag')
patch("d=sr(h)||nr[0],f=Gn(),m=await fetch(", "d=sr(h)||sr(`random`)||nr[0],f=Gn(),m=await fetch(", 'fallback board')
patch("user_tag:_isHuddle?null:(window._ppNewTag||null),", "user_tag:_isHuddle?null:(window._ppNewTag||null),board_auto:!_isHuddle&&!p&&!h,", 'send board_auto')
# the + TAG chip: hide only when all three are set; glow when a tag is needed
old_add = "function _NpAdd({hasC,open}){const[,f]=(0,_.useState)(0);(0,_.useEffect)(()=>{const on=()=>f(x=>x+1);addEventListener(`pp-np-tagset`,on);return()=>removeEventListener(`pp-np-tagset`,on)},[]);\n if(hasC&&window._ppNewTag)return null;return(0,L.jsx)(`button`,{type:`button`,className:`utag-add`,onClick:open,children:`+ tag`})}"
new_add = ("function _NpAdd({hasC,hasP,open}){const[,f]=(0,_.useState)(0),[need,setNeed]=(0,_.useState)(!1);(0,_.useEffect)(()=>{const on=()=>{f(x=>x+1);setNeed(!1)};let t=0;const nd=()=>{setNeed(!1);requestAnimationFrame(()=>setNeed(!0));clearTimeout(t);t=setTimeout(()=>setNeed(!1),2600)};addEventListener(`pp-np-tagset`,on);addEventListener(`pp-np-need`,nd);return()=>{removeEventListener(`pp-np-tagset`,on);removeEventListener(`pp-np-need`,nd);clearTimeout(t)}},[]);\n"
           " (0,_.useEffect)(()=>{if(hasP)setNeed(!1)},[hasP]);if(hasP&&hasC&&window._ppNewTag)return null;return(0,L.jsx)(`button`,{type:`button`,className:`utag-add`+(need?` need`:``),onClick:()=>{setNeed(!1);open()},children:need?`+ add a tag`:`+ tag`})}")
patch(old_add, new_add, 'add chip')
# hide the auto Random pill
patch("d&&(0,L.jsx)(`button`,{type:`button`,onClick:e=>g?m(`board`,g,e):e.stopPropagation()", "d&&!e.board_auto&&(0,L.jsx)(`button`,{type:`button`,onClick:e=>g?m(`board`,g,e):e.stopPropagation()", 'card: hide auto Random')
patch("ce&&(()=>{let e=nr.find(e=>e.name===ce)?.slug;", "ce&&!c.board_auto&&(()=>{let e=nr.find(e=>e.name===ce)?.slug;", 'post page: hide auto Random')
patch("body .lb-ic{", "@keyframes npNeed{0%,100%{box-shadow:0 0 0 0 rgba(192,132,252,0)}50%{box-shadow:0 0 0 4px rgba(192,132,252,.45),0 0 16px rgba(192,132,252,.6)}}body .utag-add.need{border-style:solid;border-color:#c084fc;color:#e9d5ff;animation:npNeed .7s ease-in-out 3}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
