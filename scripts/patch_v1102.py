#!/usr/bin/env python3
"""Patch v1101 -> v1102: the pinned and locked badges on post cards use our own line icons (same style as the
flap / chirp / share icons) instead of the 📌 and 🔒 emoji, inside the same round badge with its orange ring."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1101.js'
dst = '_deploy/assets/index-DUcNPOLc-v1102.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
SVG = lambda body: ('<svg class=\\"ri\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" '
                    'stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">' + body + '</svg>')
# a push pin, leaning over like it's stuck in the post: flat head, body, and the point
PIN = SVG('<g transform=\\"rotate(35 12 12)\\"><path d=\\"M8.5 3h7\\"/><path d=\\"M10 3v5.5L7 12.5h10l-3-4V3\\"/><path d=\\"M12 12.5V21\\"/></g>')
# a padlock: shackle, body, keyhole
LOCK = SVG('<path d=\\"M8 11V8a4 4 0 0 1 8 0v3\\"/><rect x=\\"5\\" y=\\"11\\" width=\\"14\\" height=\\"10\\" rx=\\"2.5\\"/><path d=\\"M12 15v2.5\\"/>')
patch('"SHARE": "<svg class=\\"ri ri-arrow\\"', '"PIN": "' + PIN + '", "LOCK": "' + LOCK + '", "SHARE": "<svg class=\\"ri ri-arrow\\"', 'pin and lock icons')
for v in ['e', 'c']:
    patch(v + ".pinned&&(0,L.jsx)(`span`,{className:`post-badge`,children:`📌`})",
          v + ".pinned&&(0,L.jsx)(`span`,{className:`post-badge pp-badge-ic`,title:`Pinned`,dangerouslySetInnerHTML:{__html:_ppIco(`PIN`)}})", 'pin badge ' + v)
    patch(v + ".locked&&(0,L.jsx)(`span`,{className:`post-badge`,children:`🔒`})",
          v + ".locked&&(0,L.jsx)(`span`,{className:`post-badge pp-badge-ic`,title:`Locked`,dangerouslySetInnerHTML:{__html:_ppIco(`LOCK`)}})", 'lock badge ' + v)
# icon size and colour inside the round badge (the badge keeps its orange ring)
css = ";(()=>{try{const s=document.createElement(`style`);s.textContent=`.post-badge.pp-badge-ic{color:#fbbf24}.post-badge.pp-badge-ic .ri{width:12px;height:12px;stroke-width:2.3;display:block}`;document.head.appendChild(s)}catch(e){}})();"
patch("/*ppcardfill*/", css + "/*ppcardfill*/", 'badge icon style')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
