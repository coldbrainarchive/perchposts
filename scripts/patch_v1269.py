#!/usr/bin/env python3
"""Patch v1268 -> v1269: the feed is already at the right post when the post scroller closes.
While swiping, the feed behind the scroller follows the current post; on close it's lined up again before the fade
(not 180 ms after it)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1268.js'
dst = '_deploy/assets/index-DUcNPOLc-v1269.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
SYNC = "const _fs=id=>{try{const fe=id&&document.querySelector(`[data-lp-id=\"${CSS.escape(id)}\"]`);if(fe&&!ov.contains(fe))fe.scrollIntoView({block:`center`})}catch(e){}};"
patch("const go=k=>{k=Math.max(0,Math.min(items.length-1,k));if(k!==i){i=k;swiped=!0}place(0,!0);loadNear();label();if(i>=items.length-2)more()};",
      SYNC + "const go=k=>{k=Math.max(0,Math.min(items.length-1,k));if(k!==i){i=k;swiped=!0}place(0,!0);loadNear();label();if(i>=items.length-2)more();setTimeout(()=>_fs(items[i]&&items[i].post),350)};",
      'feed follows while swiping')
patch("const cur=items[i]&&items[i].post;ov.classList.remove(`in`);",
      "const cur=items[i]&&items[i].post;if(!pendingPost&&!pendingChat)_fs(cur);ov.classList.remove(`in`);", 'line up before fade')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
