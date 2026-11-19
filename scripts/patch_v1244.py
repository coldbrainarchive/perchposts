#!/usr/bin/env python3
"""Patch v1243 -> v1244: The Cage uses the mod panel's cage line icon instead of the nest emoji:
- The Cage space pill (black icon, like the text).
- A caged bird's picture on user pills, cards, notifications, reaction lists and huddle members (red cage, #f43f5e like the pill).
- The "You're Caged!" pop-up.
The nest stays on "Post not found" (an empty nest, not The Cage)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1243.js'
dst = '_deploy/assets/index-DUcNPOLc-v1244.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
CAGE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.5V4.5"/><path d="M6 20.5V11a6 6 0 0 1 12 0v9.5"/><path d="M4 20.5h16"/><path d="M10 5.3v15.2M14 5.3v15.2"/></svg>'
# caged bird picture (every face goes through _ppB)
patch("function _ppB(x,z,k){return x&&x.u&&x.e?",
      "function _ppB(x,z,k){return x&&x.caged?(0,L.jsx)(`span`,{className:`pp-cage-av`,style:{width:z?Math.round(z*1.05):`1.05em`,height:z?Math.round(z*1.05):`1.05em`},\"aria-label\":`Caged`,dangerouslySetInnerHTML:{__html:_ppIco(`CAGE`)}}):x&&x.u&&x.e?",
      'caged bird picture = red cage icon')
# The Cage space pill
patch("children:[n.slug===`botnews`?(0,L.jsx)(`span`,{className:`pp-pn-ic`",
      "children:[n.slug===`cage`?(0,L.jsx)(`span`,{className:`pp-cage-ic`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppIco(`CAGE`)}}):n.slug===`botnews`?(0,L.jsx)(`span`,{className:`pp-pn-ic`",
      'Cage pill icon')
# the "You're Caged!" pop-up (plain DOM code, so the icon markup is inline)
patch('var icon=type==="caged"?"<span style=\\"font-size:56px;display:block;margin-bottom:14px;\\">🪹</span>"',
      'var icon=type==="caged"?"<span style=\\"display:block;width:60px;height:60px;margin:0 auto 14px;color:#f43f5e\\">' + CAGE_SVG.replace('"', '\\"').replace('<svg ', '<svg style=\\"width:100%;height:100%;display:block\\" ') + '</span>"',
      'Caged pop-up icon')
patch("body .lb-ic{", "body .pp-cage-ic{display:inline-flex;width:13px;height:13px;flex-shrink:0}body .pp-cage-ic svg{width:100%;height:100%;stroke-width:2.6}body .pp-cage-av{display:inline-flex;vertical-align:middle;color:#f43f5e;flex-shrink:0}body .pp-cage-av svg{width:100%;height:100%;display:block;stroke-width:2.3}body .lb-ic{", 'icon styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
