#!/usr/bin/env python3
"""Patch v988 -> v989: chirp preview taps + titles.
- Only a chirp, the 💬 count, View all (and the "+N more pinned" note) open the chat; tapping the preview's
  background or a section title does nothing.
- In the Top / Most replied / Latest / Media views there's no section title (the filter pill says what it
  is); Latest and Media keep their date dividers. Highlights keeps its Pinned / Top chirps / Most replied titles."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v988.js'
dst = '_deploy/assets/index-DUcNPOLc-v989.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('let _tg=_ev.target;if(_tg.closest(`.cp-filter`))return;',
      'let _tg=_ev.target;if(_tg.closest(`.cp-filter`))return;if(!_tg.closest(`.chat-msg,.chat-view-all,.pin-more-note,.chat-panel-header .feed-post-action-pill`))return;',
      'only chirps / count / View all open the chat')
patch('if(_i===_nl-1&&_nl>_nR)_st(_cpT||', 'if(_i===_nl-1&&_nl>_nR&&!_cpT)_st(_cpT||', 'no title in filtered views')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
