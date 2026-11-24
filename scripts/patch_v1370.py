#!/usr/bin/env python3
"""Patch v1369 -> v1370: open the chirps without jumping around (user's screen recording, 2026-11-24).
- Scroller -> chirps: it used to go BACK in history (closing the scroller, showing the feed, a fade), then open the
  post from the feed card — a blank flash and Safari's forward arrow. Now the scroller hands its own history entry to
  the chirps (marked to resume the scroller on back), opens them right away, and stays on top until the chirps have
  drawn, then fades out. Swiping back from the chirps still returns to the scroller.
- Posts opened any other way (notification, link, desktop card) showed the empty site page for a moment before the
  chat opened; they now keep the loading screen until the chat is up."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1369.js'
dst = '_deploy/assets/index-DUcNPOLc-v1370.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch("const goChat=id=>{pendingChat=id;close()};",
      "const goChat=id=>{if(gone)return;gone=!0;removeEventListener(`popstate`,pop);removeEventListener(`keydown`,key,!0);removeEventListener(`resize`,rs);"
      # the scroller's entry becomes the way back to it
      "try{const st={...(history.state||{})};delete st.reel;st.reelResume=id;history.replaceState(st,``)}catch(e){}"
      # put the page colour back first so the chat saves the right one to restore later
      "tcm&&prevTc&&tcm.setAttribute(`content`,prevTc);document.documentElement.classList.remove(`reel-shown`);"
      "const a=_reelChatA(id);if(a)a.click();else{try{history.pushState({},``,`/post/${id}?chat=1&via=card`);dispatchEvent(new PopStateEvent(`popstate`,{state:{}}))}catch(e){location.href=`/post/${id}?chat=1&via=card`;return}}"
      "let n=0;const t=setInterval(()=>{if(document.querySelector(`.comments-shell.chat-full`)||++n>60){clearInterval(t);ov.classList.remove(`in`);setTimeout(()=>{ov.remove();body.overflow=prevOv},180)}},50)};",
      'scroller -> chirps directly')
patch("if(!c)return(0,L.jsx)(_Bd,{});let _pv=!_cf",
      "if(!c||!c.is_huddle&&!_cf)return(0,L.jsx)(_Bd,{});let _pv=!_cf", 'no bare post page before chat')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
