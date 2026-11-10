#!/usr/bin/env python3
"""Patch v982 -> v983: tags changeover, stage 1 (names only, no data changes).
"Boards" are now "Tags" everywhere you see them: the search tab (Tags / Regions / Filters), the typed-search
section, New Post ("Select tag & country", "Tags"), the search placeholder, the not-found page, the mod
"Pin to Tag" button and the bot-feed picker. In the Tags tab, Flock, Huddles and The Cage sit in a small
"Spaces" group above the tags (they're places/views with their own rules, not topics)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v982.js'
dst = '_deploy/assets/index-DUcNPOLc-v983.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch('_stb(`boards`,`Boards`)', '_stb(`boards`,`Tags`)', 'tab name')
patch('_tab===`boards`&&(0,L.jsxs)(`div`,{className:`search-column srch-body`,children:[...g.map(x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>ee(x.slug),children:(0,L.jsx)(Ar,{boardName:x.name,small:!0})},x.slug)),',
      '_tab===`boards`&&(0,L.jsxs)(`div`,{className:`search-column srch-body`,children:[..._tagGroups(g,x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>ee(x.slug),children:(0,L.jsx)(Ar,{boardName:x.name,small:!0})},x.slug)),',
      'Spaces + Tags groups')
patch('(0,L.jsx)(`div`,{className:`search-section-label`,children:`Boards`}),g.map(e=>(0,L.jsxs)(`button`,{className:`search-s',
      '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Tags`}),g.map(e=>(0,L.jsxs)(`button`,{className:`search-s', 'typed search label')
patch('children:`Select board & country`', 'children:`Select tag & country`', 'new post heading')
patch('(0,L.jsx)(`div`,{className:`search-section-label`,children:`Boards`}),nr.filter(', '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Tags`}),nr.filter(', 'new post label')
patch('Search or filter by board, reg​ion, coun​try…', 'Search or filter by tag, reg​ion, coun​try…', 'placeholder')
patch('children:`Board not found`', 'children:`Tag not found`', 'not found title')
patch('children:`That board doesn’t exist.`', 'children:`That tag doesn’t exist.`', 'not found text')
patch('children:`📌 Pin to Board`', 'children:`📌 Pin to Tag`', 'mod pin')
patch('(0,L.jsx)(`option`,{value:``,children:`Board`})', '(0,L.jsx)(`option`,{value:``,children:`Tag`})', 'bot feed picker')

c += r'''
const _SPACES=[`activity`,`feedback`,`cage`];
function _tagGroups(list,render){const sp=list.filter(x=>_SPACES.includes(x.slug)),tg=list.filter(x=>!_SPACES.includes(x.slug)),out=[];
 const lb=(t,k)=>(0,L.jsx)(`div`,{className:`search-section-label tg-lb`,children:t},k);
 if(sp.length){out.push(lb(`Spaces`,`_lsp`));sp.forEach(x=>out.push(render(x)))}
 if(tg.length){out.push(lb(`Tags`,`_ltg`));tg.forEach(x=>out.push(render(x)))}
 return out}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.srch-body .tg-lb{flex-basis:100%;width:100%;text-align:center;padding:6px 0 2px;margin:0}.srch-body .tg-lb:first-child{padding-top:2px}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
