#!/usr/bin/env python3
"""Patch v1272 -> v1273: search dropdown Filters tab uses our line icons, not emoji.
Section labels (Flaps / Chirps / Time) and the active-filter chips in the search bar (Top flaps / Top chirps / time)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1272.js'
dst = '_deploy/assets/index-DUcNPOLc-v1273.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
ic = lambda k: "(0,L.jsx)(`span`,{className:`srch-ic`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppIco(" + k + ")}})"
for emo, key, word in [('🪽', 'BIRD', 'Flaps'), ('💬', 'CHAT', 'Chirps'), ('🕐', 'CLOCK', 'Time')]:
    patch("className:`search-section-label`,children:`%s %s`}" % (emo, word),
          "className:`search-section-label`,children:[%s,`%s`]}" % (ic('`%s`' % key), word), 'label ' + word)
patch("children:(_srt===`flaps`?`🪽 Top flaps `:`💬 Top chirps `)+(_frg===`day`?`today`:_frg===`all`?`all time`:`this week`)}",
      "children:[" + ic("_srt===`flaps`?`BIRD`:`CHAT`") + ",(_srt===`flaps`?`Top flaps `:`Top chirps `)+(_frg===`day`?`today`:_frg===`all`?`all time`:`this week`)]}", 'rank chip')
patch("children:`🕐 `+(q2&&q2.startsWith(`ago_`)?q2.slice(4)+`h ago`:q2)}",
      "children:[" + ic("`CLOCK`") + ",(q2&&q2.startsWith(`ago_`)?q2.slice(4)+`h ago`:q2)]}", 'time chip')
patch("body .lb-ic{", "body .srch-ic{display:inline-flex;width:13px;height:13px;margin-right:5px;vertical-align:-2px;flex-shrink:0}body .srch-ic svg{width:100%;height:100%;stroke-width:2.4}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
