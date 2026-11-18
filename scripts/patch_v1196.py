#!/usr/bin/env python3
"""Patch v1195 -> v1196: VIEW POST ↗ (and Open Post) in the scroller works like the chat button: Back from the post
page reopens the scroller on the post you were looking at. It also opens the post through the site's own links
(so Back behaves normally) instead of a hand-made history entry."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1195.js'
dst = '_deploy/assets/index-DUcNPOLc-v1196.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("}else if(pendingPost){const t=document.querySelector(`[data-lp-id=\"${CSS.escape(pendingPost)}\"]`);if(t&&!t.classList.contains(`feed-post-card`)){window._reelBypass=!0;t.click()}else{try{history.pushState({},``,`/post/${pendingPost}`);dispatchEvent(new PopStateEvent(`popstate`,{state:{}}))}catch(e){location.href=`/post/${pendingPost}`}}}",
      "}else if(pendingPost){try{history.replaceState({...(history.state||{}),reelResume:pendingPost},``)}catch(e){}const t=document.querySelector(`[data-lp-id=\"${CSS.escape(pendingPost)}\"]`);if(t&&!t.classList.contains(`feed-post-card`)){window._reelBypass=!0;t.click()}else{const lk=t&&t.querySelector(`a[href=\"/post/${CSS.escape(pendingPost)}\"]`);if(lk){window._reelBypass=!0;lk.click()}else{try{history.pushState({},``,`/post/${pendingPost}`);dispatchEvent(new PopStateEvent(`popstate`,{state:{}}))}catch(e){location.href=`/post/${pendingPost}`}}}}", 'View post remembers the scroller')
patch("onClickCapture:_rpOk?_ev=>{const _t=_ev.target,_cd=_ev.currentTarget;",
      "onClickCapture:_rpOk?_ev=>{if(window._reelBypass){window._reelBypass=!1;return}const _t=_ev.target,_cd=_ev.currentTarget;", 'let the post link through')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
