#!/usr/bin/env python3
"""Patch v1269 -> v1270: no iPhone scroll bar in the post scroller.
v1269 scrolled the page behind the scroller to follow the current post, which made iOS flash its scroll indicator.
Now the feed list is only shifted with a transform while the scroller is open (no real scroll); on close the transform
is cleared and the page is scrolled once, in the same frame."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1269.js'
dst = '_deploy/assets/index-DUcNPOLc-v1270.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
FF = ("let _fm=null;const _fc=()=>{if(_fm){_fm.style.transform=``;_fm.style.willChange=``;_fm=null}};"
      "const _ff=id=>{try{const fe=id&&document.querySelector(`[data-lp-id=\"${CSS.escape(id)}\"]`);if(!fe||ov.contains(fe))return;"
      "const m=fe.closest(`main`)||fe.parentElement;if(_fm&&_fm!==m)_fc();const s0=_fm?(_fm._s||0):0;_fm=m;"
      "const r=fe.getBoundingClientRect(),d=r.top+s0+r.height/2-innerHeight/2,mx=Math.max(0,document.documentElement.scrollHeight-innerHeight),"
      "T=Math.max(0,Math.min(mx,scrollY+d)),s=Math.round(T-scrollY);m._s=s;m.style.willChange=`transform`;m.style.transform=s?`translateY(${-s}px)`:``}catch(e){}};")
patch("const _fs=id=>{", FF + "const _fs=id=>{", 'transform follower')
patch("setTimeout(()=>_fs(items[i]&&items[i].post),350)", "setTimeout(()=>_ff(items[i]&&items[i].post),350)", 'follow without scrolling')
patch("const cur=items[i]&&items[i].post;if(!pendingPost&&!pendingChat)_fs(cur);",
      "const cur=items[i]&&items[i].post;_fc();if(!pendingPost&&!pendingChat)_fs(cur);", 'clear + one real scroll on close')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
