#!/usr/bin/env python3
"""Patch v1003 -> v1004: invitations / requests you have to answer can't be cleared by accident.
- They're pinned at the top of Notifications under "Needs your answer" (everything else under "Everything else").
- They stay lit (unread glow) until you answer; Clear all leaves them in place (the server keeps them too, and the
  red bubble keeps counting them until they're answered, expired or cancelled)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1003.js'
dst = '_deploy/assets/index-DUcNPOLc-v1004.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('j.map(e=>{let t=!!e.time&&e.time>ee.current&&!_nRead().has(e.id);',
      'j.length===0?null:_nOrder(j).map(e=>{if(e.__hdr)return(0,L.jsx)(`div`,{className:`n-hdr`,children:e.__hdr},`h-`+e.__hdr);let t=_nNeed(e)||!!e.time&&e.time>ee.current&&!_nRead().has(e.id);',
      'grouped list')
patch('h([]);_nAllRead(ee);', 'h(_x=>(_x||[]).filter(_nNeed));_nAllRead(ee);', 'clear keeps waiting ones')
c += r'''
function _nNeed(n){return!!(n&&n.need&&n.req&&n.req.act&&n.req.status===`pending`)}
function _nOrder(list){const need=list.filter(_nNeed);if(!need.length)return list;const rest=list.filter(n=>!_nNeed(n));
 return[{__hdr:`Needs your answer`},...need,...(rest.length?[{__hdr:`Everything else`},...rest]:[])]}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.n-hdr{margin:12px 16px 2px;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#94a3b8}.n-hdr:first-child{margin-top:8px}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
