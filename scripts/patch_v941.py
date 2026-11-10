#!/usr/bin/env python3
"""Patch v940 -> v941: drop the quick-react bar; the React button is back and opens the emoji picker sheet
(search, categories, skin tones, recents, plus the type-any-emoji box). Who-reacted list, long-press sheet
and pill pop stay."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v940.js'
dst = '_deploy/assets/index-DUcNPOLc-v941.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('v&&c&&_rxBar(e.id,c,E,C,()=>y(!1)),', '', 'remove quick bar')
patch("s&&s(e)},children:`Reply`}),",
      "s&&s(e)},children:`Reply`}),c&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:ev=>{ev.stopPropagation();_rxOpen(e.id,c,E,C,()=>y(!1))},children:`React`}),",
      'React button opens picker')
c += r'''
function _rxOpen(id,react,E,me,close){close();
 if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}
 _rxPick(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)})}
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
