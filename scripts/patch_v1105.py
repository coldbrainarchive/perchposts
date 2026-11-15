#!/usr/bin/env python3
"""Patch v1104 -> v1105: our own archive icon (a box with a lid) for archived posts, an open padlock for Unlock,
and the mod tools buttons (Pin to Tag / Pin to Forum / Unpin, Lock / Unlock, Archive / Unarchive) use the
pin, lock and archive line icons instead of emoji."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1104.js'
dst = '_deploy/assets/index-DUcNPOLc-v1105.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
SVG = lambda body: ('<svg class=\\"ri\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" '
                    'stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">' + body + '</svg>')
# an archive box: lid, box, and the handle slot (centred in its 24 box)
ARCHIVE = SVG('<g transform=\\"translate(0 -.25)\\"><rect x=\\"3\\" y=\\"4\\" width=\\"18\\" height=\\"5\\" rx=\\"1.5\\"/><path d=\\"M5 9v9.5a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V9\\"/><path d=\\"M10 13h4\\"/></g>')
# the padlock with its shackle swung open
UNLOCK = SVG('<g transform=\\"translate(0 -.5)\\"><path d=\\"M8 11V8a4 4 0 0 1 7.8-1.2\\"/><rect x=\\"5\\" y=\\"11\\" width=\\"14\\" height=\\"10\\" rx=\\"2.5\\"/><path d=\\"M12 15v2.5\\"/></g>')
patch('"SHARE": "<svg class=\\"ri ri-arrow\\"', '"ARCHIVE": "' + ARCHIVE + '", "UNLOCK": "' + UNLOCK + '", "SHARE": "<svg class=\\"ri ri-arrow\\"', 'archive and unlock icons')

# archived badge on post cards
for v in ['e', 'c']:
    patch(v + ".frozen&&(0,L.jsx)(`span`,{title:`Archived`,className:`post-badge`,children:`📦`})",
          v + ".frozen&&(0,L.jsx)(`span`,{title:`Archived`,className:`post-badge pp-badge-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`ARCHIVE`)}})", 'archived badge ' + v)

# mod tools buttons: icon + label
I = lambda k, label: "children:[(0,L.jsx)(`span`,{className:`pp-ic mt-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`" + k + "`)}}),`" + label + "`]"
for old, k, lab in [("children:`📌 Unpin`", "PIN", "Unpin"), ("children:`📌 Pin to Tag`", "PIN", "Pin to Tag"), ("children:`📍 Pin to Forum`", "PIN", "Pin to Forum"),
                    ("children:`📦 Archive`", "ARCHIVE", "Archive"), ("children:`📦 Unarchive`", "ARCHIVE", "Unarchive")]:
    i = c.index(old); j = c.rindex("(0,L.jsx)(`button`", 0, i)
    if c.count(old) != 1: print('FAIL', lab); sys.exit(1)
    c = c[:j] + "(0,L.jsxs)" + c[j + len("(0,L.jsx)"):i] + I(k, lab) + c[i + len(old):]; print('OK: mod tool', lab)
old = "children:c.locked?`🔓 Unlock`:`🔒 Lock`}"
i = c.index(old); j = c.rindex("(0,L.jsx)(`button`", 0, i)
c = c[:j] + "(0,L.jsxs)" + c[j + len("(0,L.jsx)"):i] + "children:[(0,L.jsx)(`span`,{className:`pp-ic mt-ic`,dangerouslySetInnerHTML:{__html:_ppIco(c.locked?`UNLOCK`:`LOCK`)}}),c.locked?`Unlock`:`Lock`]}" + c[i + len(old):]; print('OK: mod tool Lock/Unlock')

# icon size and spacing inside the mod tool pills
patch(".post-badge.pp-badge-ic{color:#fbbf24;padding:0!important}",
      ".post-badge.pp-badge-ic{color:#fbbf24;padding:0!important}.mod-tool .mt-ic{margin:0 5px 0 -2px}.mod-tool .mt-ic .ri{width:13px;height:13px;stroke-width:2.3;display:block}", 'mod tool icon style')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
