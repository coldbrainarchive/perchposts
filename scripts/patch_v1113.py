#!/usr/bin/env python3
"""Patch v1112 -> v1113: the "Waiting" tag on invited birds (huddle members list) uses our own grey hourglass icon
instead of the ⏳ emoji."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1112.js'
dst = '_deploy/assets/index-DUcNPOLc-v1113.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
HG = ('<svg class=\\"ri\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">'
      '<path d=\\"M6.5 3h11M6.5 21h11\\"/><path d=\\"M7.5 3v2.5c0 2.2 1.7 3.6 4.5 6.5 2.8-2.9 4.5-4.3 4.5-6.5V3\\"/><path d=\\"M7.5 21v-2.5c0-2.2 1.7-3.6 4.5-6.5 2.8 2.9 4.5 4.3 4.5 6.5V21\\"/><path d=\\"M10 18.5h4\\"/></svg>')
patch('"SHARE": "<svg class=\\"ri ri-arrow\\"', '"HOURGLASS": "' + HG + '", "SHARE": "<svg class=\\"ri ri-arrow\\"', 'hourglass icon')
patch('const _PPE={"👑":`CROWN`,', 'const _PPE={"⏳":`HOURGLASS`,"⌛":`HOURGLASS`,"👑":`CROWN`,', 'hourglass label')
patch("(0,L.jsx)(`span`,{className:`hx-tag`,children:`⏳ Waiting`},`w`)", "(0,L.jsx)(`span`,{className:`hx-tag hx-wait`,children:_ppLbl(`⏳ Waiting`)},`w`)", 'waiting tag')
patch("body .hx-tag .lb-ic .ri{color:#c084fc}", "body .hx-tag .lb-ic .ri{color:#c084fc}body .hx-tag.hx-wait .lb-ic .ri{color:#94a3b8}", 'grey hourglass')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
