#!/usr/bin/env python3
"""Patch v958 -> v959: the "↓ N new" catch-up pill
- is only a notice now: tapping it does nothing, so you read the missed chirps
  in order instead of jumping to the bottom;
- never follows you out of the chat: it's removed when the chat closes, the page changes, or the chat
  window leaves the screen (checked on every render, on back/forward, and twice a second while shown)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v958.js'
dst = '_deploy/assets/index-DUcNPOLc-v959.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('if(!on){if(s&&s.win)delete _rd[p];return s&&s.mode===`resume`?s.snap:null}',
      'if(!on){if(s&&s.pill){s.pill.remove();s.pill=null}if(s&&s.win)delete _rd[p];return s&&s.mode===`resume`?s.snap:null}', 'close removes pill')
patch('const show=n>0&&Math.abs(w.scrollTop)>200&&!live&&w.isConnected;',
      'const show=n>0&&Math.abs(w.scrollTop)>200&&!live&&_rdOn(w);', 'show only in an open chat')
patch("if(!s.pill){const q=document.createElement(`button`);q.type=`button`;q.className=`rd-pill`;\n  q.onclick=()=>w.scrollTo({top:0,behavior:matchMedia(`(prefers-reduced-motion: reduce)`).matches?`auto`:`smooth`});\n  document.body.appendChild(q);s.pill=q}",
      "if(!s.pill){const q=document.createElement(`div`);q.className=`rd-pill`;q.setAttribute(`aria-live`,`polite`);document.body.appendChild(q);s.pill=q;\n  const iv=setInterval(()=>{if(!s.pill||s.pill!==q){clearInterval(iv);return}if(!_rdOn(w)){q.remove();if(s.pill===q)s.pill=null;clearInterval(iv)}},500)}",
      'pill is a notice + watcher')
c += r'''
function _rdOn(w){return!!(w&&w.isConnected&&w.offsetParent&&!w.closest(`.chat-preview`)&&w.getClientRects().length)}
try{addEventListener(`popstate`,()=>{for(const k in _rd){const s=_rd[k];if(s&&s.pill){s.pill.remove();s.pill=null}}})}catch(e){}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.rd-pill{cursor:default;-webkit-tap-highlight-color:transparent;user-select:none;-webkit-user-select:none}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
