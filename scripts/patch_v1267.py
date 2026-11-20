#!/usr/bin/env python3
"""Patch v1265 -> v1267 (v1266 + the fix runs before paint, no one-frame flash): opening a chirp (action sheet / who-reacted list) near the top of the chat no longer hides its top.
The chat window is column-reverse (anchored at the bottom), so a growing chirp pushes up under the title bar;
after it opens, scroll just enough to bring the chirp's top back into view."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1265.js'
dst = '_deploy/assets/index-DUcNPOLc-v1267.js'
c = open(src, encoding='utf-8').read()
c += r"""
;(()=>{try{
  const fix=el=>{const w=el.closest(`.chat-window`);if(!w)return;const m=el.closest(`[data-comment-id]`)||el.closest(`.chat-msg-body`);if(!m)return;
    const go=()=>{if(!m.isConnected)return;const wr=w.getBoundingClientRect(),mr=m.getBoundingClientRect(),d=wr.top+10-mr.top;if(d>0){w.scrollTop-=d;const mx=w.scrollHeight-w.clientHeight;if(mx-Math.abs(w.scrollTop)<80)w.scrollTop=-mx}};
    go();requestAnimationFrame(go);setTimeout(go,260)};
  new MutationObserver(ms=>{for(const r of ms)for(const n of r.addedNodes){if(n.nodeType!==1)continue;const t=n.matches(`.chat-action-sheet,.rx-who`)?n:n.querySelector&&n.querySelector(`.chat-action-sheet,.rx-who`);if(t){fix(t);return}}}).observe(document.body,{childList:!0,subtree:!0});
}catch(e){console.error(e)}})();
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
