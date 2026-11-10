#!/usr/bin/env python3
"""Patch v1001 -> v1002: going back after opening a notification.
- A notification that opens a chat no longer leaves a copy of the post page under it (that copy had the same
  address, so the first swipe back looked like it froze), and the clean-up ~2s later keeps the chat's address.
- Swiping back (or the browser's back) returns to the page you were on with the notifications panel open again,
  scrolled to where you were."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1001.js'
dst = '_deploy/assets/index-DUcNPOLc-v1002.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('if(a||_nc||_sy)history.replaceState(history.state,``,location.pathname);history.pushState(history.state,``,location.pathname+`?chat=1`);window._cfPushed=!0;O.current=!0;_setCF(!0)}',
      'if(a||_nc||_sy){history.replaceState(history.state,``,location.pathname+`?chat=1`);window._cfPushed=!1}else{history.pushState(history.state,``,location.pathname+`?chat=1`);window._cfPushed=!0}O.current=!0;_setCF(!0)}',
      'notification chat replaces in place')
patch('setTimeout(()=>o(`/post/${r}`,{replace:!0}),1800)',
      'setTimeout(()=>o(`/post/${r}`+(new URLSearchParams(location.search).get(`chat`)===`1`?`?chat=1`:``),{replace:!0}),1800)',
      'clean-up keeps chat address')
patch('onClick:()=>{_nMark(e);a()}', 'onClick:_ev=>{_nTap(_ev);_nMark(e);a()}', 'remember panel on tap')
c += r'''
function _nScroller(el){let s=el&&el.parentElement;while(s&&s!==document.body&&!(s.scrollHeight>s.clientHeight&&/(auto|scroll)/.test(getComputedStyle(s).overflowY)))s=s.parentElement;return s&&s!==document.body?s:null}
function _nTap(ev){try{const s=_nScroller(ev.currentTarget);history.replaceState({...(history.state||{}),ppNotif:{y:s?s.scrollTop:0}},``)}catch(e){}}
addEventListener(`popstate`,()=>{const n=history.state&&history.state.ppNotif;if(!n)return;
 try{const st={...history.state};delete st.ppNotif;history.replaceState(st,``)}catch(e){}
 setTimeout(()=>{const b=document.querySelector(`.nav-user-pill`);if(!b)return;b.click();let k=0;
  const t=setInterval(()=>{k++;const a=document.querySelector(`a[href^="/post/"][style*="border-radius: 20px"]`),s=a&&_nScroller(a);if(s){s.scrollTop=n.y||0;clearInterval(t)}if(k>60)clearInterval(t)},50)},80)});
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
