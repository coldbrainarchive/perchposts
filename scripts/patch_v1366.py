#!/usr/bin/env python3
"""Patch v1365 -> v1366: leaving a chat back into the post scroller left a grey band behind Safari's bottom toolbar
(iPhone): Safari kept the chat's grey theme-color even after it was set back. On leaving the chat, the theme-color
tag is swapped for a fresh copy (now, ~0.3s and ~0.9s later) so Safari re-reads it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1365.js'
dst = '_deploy/assets/index-DUcNPOLc-v1366.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("_tc&&(_tc.content=_tv);_h.classList.remove(`chat-open`,`chat-kb`,`chat-crios`);",
      "_tc&&(_tc.content=_tv);_h.classList.remove(`chat-open`,`chat-kb`,`chat-crios`);_ppTcKick();", 'kick on leave')
c += r"""
// Safari (iPhone) can keep a theme-color it has already painted behind its toolbars; a fresh <meta> makes it re-read
function _ppTcKick(){const k=()=>{try{const m=document.querySelector(`meta[name="theme-color"]`);if(!m)return;const n=m.cloneNode(!0);n.content=document.documentElement.classList.contains(`reel-shown`)?`#000000`:m.content;m.replaceWith(n)}catch(e){}};k();setTimeout(k,300);setTimeout(k,900)}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
