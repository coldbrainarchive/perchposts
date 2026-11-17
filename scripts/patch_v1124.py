#!/usr/bin/env python3
"""Patch v1123 -> v1124: a chirp's who-reacted sheet lists worm givers on the All tab too.
One row per person: their emoji, then 🪱 and how many worms they gave. The All count includes worms."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1123.js'
dst = '_deploy/assets/index-DUcNPOLc-v1124.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# a row can carry worms (r.w) after its emoji
patch("(0,L.jsx)(`span`,{className:`rx-qs`,children:r.qs.join(` `)})]},i)}",
      "(0,L.jsxs)(`span`,{className:`rx-qs`,children:[r.qs.join(` `),r.w?(0,L.jsxs)(`span`,{className:`pr-w rx-w`,children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),r.w]}):null]})]},i)}",
      'rows can show worms')
# All tab: emoji reactors merged with worm givers
patch("function _rxSheet(ee,sel,set,go,cid){const tot=ee.reduce((a,[,ids])=>a+ids.length,0),",
      r'''function _RxAll({ee,cid,go}){const[g,set]=(0,_.useState)(null),wn=cid?_ppWorm.n(_ppWorm.key(`c`,cid)):0;
 (0,_.useEffect)(()=>{if(!cid)return;let on=!0;const ld=()=>fetch(`${R}/worm-givers?comment_id=${encodeURIComponent(cid)}`,{headers:er()}).then(r=>r.ok?r.json():{givers:[]}).then(d=>on&&set(d.givers||[])).catch(()=>on&&set([]));
  ld();const u=_ppWorm.sub(_ppWorm.key(`c`,cid),()=>setTimeout(ld,600));return()=>{on=!1;u()}},[cid]);
 const rows=_rxGroup(ee,`all`).map(r=>({...r}));
 for(const p of g||[]){const r=rows.find(x=>x.name===p.username);if(r)r.w=p.c;else rows.push({name:p.username,qs:[],w:p.c})}
 if(!rows.length)return(0,L.jsx)(`div`,{className:`cp-empty`,children:wn&&!g?`Loading…`:`No reactions yet`});
 return(0,L.jsx)(L.Fragment,{children:rows.map((r,i)=>_rxRow(r,i,0,0,go))})}
function _rxSheet(ee,sel,set,go,cid){const tot=ee.reduce((a,[,ids])=>a+ids.length,0)+(cid?_ppWorm.n(_ppWorm.key(`c`,cid)):0),''',
      'All tab merges worm givers')
patch("children:cur===`🪱`?(0,L.jsx)(_WormGivers,{kind:`c`,id:cid,go:go?n=>{set(null);go(n)}:null}):_rxGroup(ee,cur).map(",
      "children:cur===`🪱`?(0,L.jsx)(_WormGivers,{kind:`c`,id:cid,go:go?n=>{set(null);go(n)}:null}):cur===`all`?(0,L.jsx)(_RxAll,{ee,cid,go:go?n=>{set(null);go(n)}:null}):_rxGroup(ee,cur).map(",
      'All tab uses it')
patch("body .lb-ic{", "body .rx-qs .rx-w{display:inline-flex;align-items:center;gap:3px;margin-left:6px;vertical-align:middle}body .rx-qs .rx-w .ri.wemo{font-size:14px}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
