#!/usr/bin/env python3
"""Patch v1380 -> v1381: the open-post action row copies the scroller dock exactly (measured side by side):
colour fades in over .15s (no instant switch, no icon pop), 12px text, 18px bird pulled 2px in, 14px chirp,
17px worm, 10px share arrow with a 5px gap."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1380.js'
dst = '_deploy/assets/index-DUcNPOLc-v1381.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
# no pop (the scroller dock never pops)
patch("if(!mine)_ppFlapAnim(b);setPop(!0);setTimeout(()=>setPop(!1),260);onFlap(ev)", "if(!mine)_ppFlapAnim(b);onFlap(ev)", 'no pop')
patch("body .lb-ic{",
 "body .ch-dock .ch-db{font-size:12px;line-height:12px;letter-spacing:.02em;font-weight:800;transition:color .15s,background .15s}"
 "body .ch-dock .ch-db .i{transition:none;transform:none!important}"
 "body .ch-dock .ch-db.ch-fl .i{margin-right:-2px}body .ch-dock .ch-db.ch-fl .pp-ic .ri{width:18px;height:18px;stroke-width:2.1}"
 "body .ch-dock .ch-db.ch-ch .pp-ic .ri{width:14px;height:14px}body .ch-dock .ch-db.ch-wm .pp-ic .ri{width:17px;height:17px}"
 "body .ch-dock .ch-db.ch-sh{gap:5px}body .ch-dock .ch-db.ch-sh .pp-ic .ri{width:10px;height:10px}body .ch-dock .ch-db.ch-sh.done .pp-ic .ri{width:14px;height:14px}"
 "body .ch-dock .ch-db .n{transition:color .15s}"
 "body .lb-ic{", 'css')
# keep the icon HTML objects stable: React 19 re-sets innerHTML whenever the dangerouslySetInnerHTML object changes,
# which replaced the bird mid-flap (the wings never moved)
i = c.index("function _ChDock({post:c,n,score,mine,onFlap,chat,grab})"); j = c.index("\n  grab]})}", i)
body = c[i:j]
import re
n0 = body.count("{__html:_ppIco(`")
body = re.sub(r"\{__html:_ppIco\(`([A-Z]+)`\)\}", r"_chIH(`\1`)", body)
k = body.index("{__html:`<svg"); k2 = body.index("`}", k) + 2
body = body[:k] + "_chIH(`TICK`," + body[k+len("{__html:"):k2-1] + ")" + body[k2:]
c = c[:i] + body + c[j:]
print('stable icons', n0)
c += "\nconst _chIHm=new Map();function _chIH(k,h){let o=_chIHm.get(k);if(!o){o={__html:h||_ppIco(k)};_chIHm.set(k,o)}return o}\n"
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
