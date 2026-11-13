#!/usr/bin/env python3
"""Patch v1042 -> v1043: going back from a chat opened with the full-screen view's 💬 button returns to the
full-screen view on that same post (instead of the plain feed).
How: before following the chat link, the feed's history entry is tagged with reelResume=<post id>. When back lands on
a tagged entry, the tag is removed and the view reopens on that post's card once the feed has drawn it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1042.js'
dst = '_deploy/assets/index-DUcNPOLc-v1043.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('else if(pendingChat){const a=_reelChatA(pendingChat);',
      'else if(pendingChat){try{history.replaceState({...(history.state||{}),reelResume:pendingChat},``)}catch(e){}const a=_reelChatA(pendingChat);',
      'tag feed entry')
c += r'''
;(()=>{try{addEventListener(`popstate`,()=>{try{const st=history.state;const id=st&&st.reelResume;if(!id)return;
 const rest={...st};delete rest.reelResume;try{history.replaceState(rest,``)}catch(e){}
 let n=0;const t=setInterval(()=>{const el=document.querySelector(`[data-lp-id="${CSS.escape(id)}"]`);
  if(el&&el.getClientRects().length){clearInterval(t);if(!document.querySelector(`.reel`)){try{el.scrollIntoView({block:`center`})}catch(e){}_reelOpen(el)}}
  else if(++n>50)clearInterval(t)},100)}catch(e){}})}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
