#!/usr/bin/env python3
"""Patch v997 -> v998: the huddle page's top card matches the Huddles space cards.
- No owner pill / HUDDLES tag above the title (the owner has the 👑 on their circle and in Members).
- No box-inside-a-box: the title and the member row sit straight on the card, which uses the inbox card's
  rounding, tint and border. The title is a bit bigger.
- Invite / Remove / Leave stay as they are; the time pill says "Started 4d ago"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v997.js'
dst = '_deploy/assets/index-DUcNPOLc-v998.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('{className:`content-card feed-post-card`,style:{marginBottom:16},children:[(0,L.jsx)(`div`,{className:`feed-post-board-row`',
      '{className:c.is_huddle?`content-card feed-post-card hp-card`:`content-card feed-post-card`,style:{marginBottom:16},children:[!c.is_huddle&&(0,L.jsx)(`div`,{className:`feed-post-board-row`',
      'no pills, card class')
patch('(c.title||e)&&(0,L.jsx)(`div`,{style:{border:`1px solid rgba(148,163,184,0.15)`,borderRadius:12,background:`#1a1d27`,padding:`14px 16px`,marginBottom:t?10:0}',
      '(c.title||e)&&(0,L.jsx)(`div`,{className:c.is_huddle?`hp-body`:void 0,style:c.is_huddle?{padding:`0 2px`,marginBottom:6}:{border:`1px solid rgba(148,163,184,0.15)`,borderRadius:12,background:`#1a1d27`,padding:`14px 16px`,marginBottom:t?10:0}',
      'no inner box')
patch('(0,L.jsx)(`span`,{className:`feed-post-action-pill`,style:{marginLeft:`auto`,cursor:`default`},children:Un(c.created_at)})',
      '(0,L.jsx)(`span`,{className:`feed-post-action-pill`,style:{marginLeft:`auto`,cursor:`default`},children:c.is_huddle?`Started ${Un(c.created_at)}`:Un(c.created_at)})',
      'Started time')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.hp-card{border-radius:20px!important;background:#171a21!important;border:1px solid #262a35!important;padding-top:18px!important}
.hp-body h2{font-size:21px!important;margin-bottom:10px!important}
.hp-body .hx-row{margin-top:0;padding-left:0}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
