#!/usr/bin/env python3
"""Patch v959 -> v960:
- One pill only: the live "↓ N new chirps" jump pill (v927) is gone. Chirps that arrive while you're scrolled
  up just add to the "↓ N new" catch-up count (it counts every loaded chirp you haven't seen yet).
- The NEW divider no longer flashes in the post page preview after leaving the chat."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v959.js'
dst = '_deploy/assets/index-DUcNPOLc-v960.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('st.unread=(st.unread||0)+1;pill(w,st);return}', 'return}', 'no live jump pill')
patch('if(!on){if(s&&s.pill){s.pill.remove();s.pill=null}if(s&&s.win)delete _rd[p];return s&&s.mode===`resume`?s.snap:null}',
      'if(!on){if(s&&s.pill){s.pill.remove();s.pill=null}if(s&&s.win)delete _rd[p];return null}', 'no divider outside the chat')
patch('if(_rdS&&_e.created_at>_rdS&&', 'if(!_pv&&_rdS&&_e.created_at>_rdS&&', 'divider only in chat')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
