#!/usr/bin/env python3
"""Patch v960 -> v961: when someone chirps while you're scrolled up reading, the "↓ N new" pill flashes once
(a quick pulse + glow) as its count goes up, so you notice new chirps landing at the bottom. Reading
(count going down) and opening the chat don't flash."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v960.js'
dst = '_deploy/assets/index-DUcNPOLc-v961.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# Remember the newest chirp time; a newer one arriving = new chirps (not reading, not older pages)
patch('function _rdPill(p,w){const s=_rd[p];if(!s)return;const seen=_rdGet(p);',
      'function _rdPill(p,w){const s=_rd[p];if(!s)return;const seen=_rdGet(p);'
      'let _nw=null;w.querySelectorAll(`.chat-msg[data-t]`).forEach(m=>{const t=m.dataset.t;if(!_nw||t>_nw)_nw=t});'
      'const _grew=s.newest!=null&&_nw&&_nw>s.newest;if(_nw)s.newest=_nw;',
      'track newest')
patch('s.pill.textContent=`↓ ${n} new`}',
      's.pill.textContent=`↓ ${n} new`;'
      'if(_grew&&s.lastN!=null&&n>s.lastN&&!matchMedia(`(prefers-reduced-motion: reduce)`).matches)s.pill.animate('
      '[{transform:`translateX(-50%) scale(1)`},{transform:`translateX(-50%) scale(1.18)`,boxShadow:`0 0 0 6px rgba(192,132,252,.55),0 0 22px rgba(192,132,252,.9)`,offset:.3},{transform:`translateX(-50%) scale(1)`}],'
      '{duration:650,easing:`cubic-bezier(.3,.7,.3,1)`});s.lastN=n}',
      'flash on new')
# Pill hidden -> forget the last count so a fresh appearance from a new chirp also flashes
patch('if(!show){if(s.pill){s.pill.remove();s.pill=null}return}',
      'if(!show){if(s.pill){s.pill.remove();s.pill=null}s.lastN=0;return}',
      'reset count when hidden')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
