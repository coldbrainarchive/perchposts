#!/usr/bin/env python3
"""Patch v1367 -> v1368: Safari (iPhone) only re-reads the page colour for the strip under its toolbar when the
URL changes (pushState / popstate), which happens before the scroller / chat switch colour — so the strip showed the
previous screen's colour (recording: black in the chat, the chat's grey back in the scroller). After the page colour
changes (reel-shown / chat-open on <html>), re-set the same URL with replaceState so Safari samples the new colour.
Also drops v1367's black block under the toolbar (Safari doesn't paint page content there)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1367.js'
dst = '_deploy/assets/index-DUcNPOLc-v1368.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("html.reel-shown body::after{content:\"\";position:fixed;left:0;right:0;top:100%;height:70vh;background:#000;pointer-events:none;z-index:9499}", "", 'drop black block')
c += r"""
// iPhone Safari samples the page colour for the strip under its toolbar on URL changes only; re-set the same URL
// after the scroller / chat change the page colour so the strip follows (user's screen recording, 2026-11-24)
(function(){try{let was=``,t1=0,t2=0;const key=()=>{const c=document.documentElement.classList;return(c.contains(`reel-shown`)?`r`:``)+(c.contains(`chat-open`)?`c`:``)};
 const kick=()=>{try{history.replaceState(history.state,``,location.href)}catch(e){}};
 new MutationObserver(()=>{const k=key();if(k===was)return;was=k;clearTimeout(t1);clearTimeout(t2);t1=setTimeout(()=>requestAnimationFrame(kick),60);t2=setTimeout(kick,450)}).observe(document.documentElement,{attributes:!0,attributeFilter:[`class`]})}catch(e){}})();
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
