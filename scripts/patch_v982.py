#!/usr/bin/env python3
"""Patch v981 -> v982: the chat's ‹ arrow (and its title) always goes to the post page; swiping back / the
browser's back goes wherever you came from.
- Opened from the post page (the chat is a history step on top of it): ‹ steps back to it, as before.
- Opened straight from a post card's 💬 (no post page underneath): ‹ swaps the chat for the post page in
  place, so the post page then sits where the chat was and swiping back from it goes to the feed."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v981.js'
dst = '_deploy/assets/index-DUcNPOLc-v982.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('_closeC=()=>history.back()',
      '_closeC=()=>{if(window._cfPushed){history.back()}else{history.replaceState(history.state,``,location.pathname);_setCF(!1)}}', 'arrow goes to post page')
patch('history.pushState(history.state,``,location.pathname+`?chat=1`);O.current=!0;_setCF(!0)}',
      'history.pushState(history.state,``,location.pathname+`?chat=1`);window._cfPushed=!0;O.current=!0;_setCF(!0)}', 'opened from post page')
patch('if(new URLSearchParams(location.search).get(`via`)===`card`)history.replaceState(history.state,``,location.pathname+`?chat=1`);else{history.replaceState(history.state,``,location.pathname);history.pushState(history.state,``,location.pathname+`?chat=1`)}',
      'if(new URLSearchParams(location.search).get(`via`)===`card`){history.replaceState(history.state,``,location.pathname+`?chat=1`);window._cfPushed=!1}else{history.replaceState(history.state,``,location.pathname);history.pushState(history.state,``,location.pathname+`?chat=1`);window._cfPushed=!0}',
      'opened from card / refresh')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
