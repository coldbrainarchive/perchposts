#!/usr/bin/env python3
"""Patch v933 -> v934:
1. Mobile: refreshing while in the full-screen chirp chat stays in the chat. Opening the chat now pushes
   ?chat=1 (was the same URL); on load with ?chat=1 (phone widths) the chat reopens, re-creating the
   post-page history entry underneath so Back still returns to the post.
2. Pinned chirps glow in their author's colour (--gc on the pinned chirp body), as does the flash when you
   jump to a pinned chirp (was always purple).
3. Replies use the colour of the bird being replied to: the quoted bar inside a reply chirp
   (.chat-quote-bar / .chat-quote-name) and the "replying to" bar above the compose box
   (.chat-reply-preview, its name) - via --rc set from the quoted bird's name colour.
"""
import re, sys
src = '_deploy/assets/index-DUcNPOLc-v933.js'
dst = '_deploy/assets/index-DUcNPOLc-v934.js'
c = open(src, encoding='utf-8').read()
errors = []
def patch(old, new, label):
    global c
    n = c.count(old)
    if n != 1: errors.append(f'FAIL ({label}): {n}')
    else: c = c.replace(old, new); print('OK: ' + label)
# 1. refresh stays in chat
patch("history.pushState(history.state,``,location.href);O.current=!0;_setCF(!0)},_closeC=()=>history.back(),",
      "history.pushState(history.state,``,location.pathname+`?chat=1`);O.current=!0;_setCF(!0)},_closeC=()=>history.back(),", 'open chat pushes ?chat=1')
patch("(0,_.useEffect)(()=>{let _f=()=>_setCF(!1);window.addEventListener(`popstate`,_f);return()=>window.removeEventListener(`popstate`,_f)},[]);",
      "(0,_.useEffect)(()=>{let _f=()=>_setCF(!1);window.addEventListener(`popstate`,_f);return()=>window.removeEventListener(`popstate`,_f)},[]);"
      "(0,_.useEffect)(()=>{if(new URLSearchParams(location.search).get(`chat`)!==`1`)return;if(!(window.matchMedia&&matchMedia(`(max-width: 900px)`).matches)){history.replaceState(history.state,``,location.pathname);return}"
      "history.replaceState(history.state,``,location.pathname);history.pushState(history.state,``,location.pathname+`?chat=1`);_cyR.current=0;O.current=!0;_setCF(!0)},[]);",
      'reopen chat on refresh')
# 2. pinned glow in author colour
patch('.chat-msg-body.chat-pinned{box-shadow:0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)}',
      '.chat-msg-body.chat-pinned{box-shadow:0 0 0 4px rgba(var(--gc,192,132,252),0.6),0 0 20px rgba(var(--gc,192,132,252),0.8)}', 'pinned glow var')
patch('if(_gm&&!e.classList.contains(`chat-pinned`))', 'if(_gm)', 'jump flash on pinned uses author colour')
# 3. replies in the replied-to bird's colour
reps = [
 ('background: rgba(192,132,252,0.22);\n        border-bottom: 1px solid rgba(192,132,252,0.18);', 'background: rgba(var(--rc,192,132,252),0.22);\n        border-bottom: 1px solid rgba(var(--rc,192,132,252),0.18);', 'quote bar'),
 ('.chat-quote-name {\n        display: block;\n        font-size: 11px;\n        font-weight: 700;\n        color: #c084fc;', '.chat-quote-name {\n        display: block;\n        font-size: 11px;\n        font-weight: 700;\n        color: rgb(var(--rc,192,132,252));', 'quote name'),
 ('border-radius: 10px;\n        border-left: 3px solid #c084fc;\n      }', 'border-radius: 10px;\n        border-left: 3px solid rgb(var(--rc,192,132,252));\n      }', 'reply preview bar'),
 ('.chat-reply-preview-name {\n        display: block;\n        font-size: 11px;\n        font-weight: 700;\n        color: #c084fc;', '.chat-reply-preview-name {\n        display: block;\n        font-size: 11px;\n        font-weight: 700;\n        color: rgb(var(--rc,192,132,252));', 'reply preview name'),
]
for o, n, l in reps: patch(o, n, l)
JS = r'''
;(()=>{try{
const cache=new Map();
const toRGB=col=>{if(cache.has(col))return cache.get(col);const sp=document.createElement('span');sp.style.cssText='position:absolute;visibility:hidden;color:'+col;document.body.appendChild(sp);const m=(getComputedStyle(sp).color||'').match(/(\d+),\s*(\d+),\s*(\d+)/);sp.remove();const v=m?m[1]+','+m[2]+','+m[3]:'192,132,252';cache.set(col,v);return v};
const run=()=>{
 document.querySelectorAll('.chat-msg-body.chat-pinned').forEach(b=>{const mt=b.querySelector('.chat-msg-meta');if(!mt)return;const v=window._rgbOf(mt);if(b.dataset.gc!==v){b.dataset.gc=v;b.style.setProperty('--gc',v)}});
 document.querySelectorAll('.chat-quote-bar,.chat-reply-preview').forEach(el=>{const nm=el.querySelector('.chat-quote-name,.chat-reply-preview-name');if(!nm)return;const t=(nm.textContent||'').trim();if(el.dataset.rcn===t)return;el.dataset.rcn=t;
  const col=_ncol(t.replace(/^(Replying to|↩︎?|@)\s*/i,''));if(col==='transparent'){el.style.removeProperty('--rc');return}el.style.setProperty('--rc',toRGB(col))})};
let q=0;new MutationObserver(()=>{if(q)return;q=1;requestAnimationFrame(()=>{q=0;run()})}).observe(document.body,{childList:true,subtree:true,characterData:true});run();
}catch(e){}})();
'''
if errors: print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(c + JS); print('Wrote ' + dst)
