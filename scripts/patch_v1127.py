#!/usr/bin/env python3
"""Patch v1126 -> v1127: worms get their own row in who-reacted lists. A person's reaction row stays as it was; right
below it is a second row with their name and 🪱 N (the same look as the 🪱 tab). Worm-only people get just that row.
Your own rows (both) come first in the list under a tapped chirp."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1126.js'
dst = '_deploy/assets/index-DUcNPOLc-v1127.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# one helper: reaction rows, each followed by that person's worm row; worm-only people at the end
patch("function _rxWho(ee,only,go,more,wg){let rows=_rxGroup(ee,only).map(r=>({...r}));for(const p of wg||[]){const r=rows.find(x=>x.name===p.username);if(r)r.w=p.c;else rows.push({name:p.username,qs:[],w:p.c})}if(!rows.length)return null;const _mn=Qn()?.username;if(_mn){const k=rows.findIndex(r=>r.name===_mn);if(k>0)rows=[rows[k],...rows.slice(0,k),...rows.slice(k+1)]}",
      "function _rxMix(rows,wg){const out=[],left=new Map((wg||[]).map(p=>[p.username,p.c]));for(const r of rows){out.push(r);if(r.name&&left.has(r.name)){out.push({name:r.name,qs:[],w:left.get(r.name)});left.delete(r.name)}}for(const[n,w]of left)out.push({name:n,qs:[],w});return out}\n"
      "function _rxWho(ee,only,go,more,wg){let rows=_rxMix(_rxGroup(ee,only),wg);if(!rows.length)return null;const _mn=Qn()?.username;if(_mn&&rows.some(r=>r.name===_mn))rows=[...rows.filter(r=>r.name===_mn),...rows.filter(r=>r.name!==_mn)];",
      'separate worm rows (list under a chirp)')
patch(" const rows=_rxGroup(ee,`all`).map(r=>({...r}));\n for(const p of g||[]){const r=rows.find(x=>x.name===p.username);if(r)r.w=p.c;else rows.push({name:p.username,qs:[],w:p.c})}",
      " const rows=_rxMix(_rxGroup(ee,`all`),g);", 'separate worm rows (All tab)')
# a worm row looks like the 🪱 tab's rows
patch("(0,L.jsxs)(`span`,{className:`rx-qs`,children:[r.qs.join(` `),r.w?(0,L.jsxs)(`span`,{className:`pr-w rx-w`,children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),r.w]}):null]})]},i)}",
      "r.w?(0,L.jsx)(`span`,{className:`pr-did`,children:(0,L.jsxs)(`span`,{className:`pr-w`,children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),r.w]})}):(0,L.jsx)(`span`,{className:`rx-qs`,children:r.qs.join(` `)})]},i)}",
      'worm row look')
# drop the v1126 chip styles
i = c.index("body .rx-qs{display:inline-flex;align-items:center}"); j = c.index("body .lb-ic{", i)
c = c[:i] + "body .rx-who .pr-did .pr-w{font-size:12px}body .rx-who .pr-did .ri.wemo{font-size:13px}" + c[j:]; print('OK: styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
