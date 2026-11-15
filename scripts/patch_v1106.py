#!/usr/bin/env python3
"""Patch v1105 -> v1106: mod controls all match, in the site purple.
- Mod tools: the label gets a shield icon, Delete a trash icon; pills, label and divider are purple (Delete stays red).
- Post badges (pinned / locked / archived): purple ring and icon instead of orange.
- Mod panel, Deleted and Archived lists: View / Restore / Unarchive / Show-Hide / Delete / Delete All become the same
  pill buttons with line icons (same style as flap, chirp and share)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1105.js'
dst = '_deploy/assets/index-DUcNPOLc-v1106.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
SVG = lambda body: ('<svg class=\\"ri\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" '
                    'stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">' + body + '</svg>')
ICONS = {
  "TRASH": SVG('<path d=\\"M4 7h16\\"/><path d=\\"M9 7V4.5h6V7\\"/><path d=\\"M6.2 7l.9 12.2a2 2 0 0 0 2 1.8h5.8a2 2 0 0 0 2-1.8L17.8 7\\"/><path d=\\"M10 11v6M14 11v6\\"/>'),
  "SHIELD": SVG('<path d=\\"M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z\\"/><path d=\\"M9 12l2 2 4-4\\"/>'),
  "RESTORE": SVG('<path d=\\"M4.5 12a7.5 7.5 0 1 0 2.2-5.3L4.5 9\\"/><path d=\\"M4.5 4.5V9H9\\"/>'),
  "EYE": SVG('<path d=\\"M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z\\"/><circle cx=\\"12\\" cy=\\"12\\" r=\\"3\\"/>'),
  "EYEOFF": SVG('<path d=\\"M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z\\"/><circle cx=\\"12\\" cy=\\"12\\" r=\\"3\\"/><path d=\\"M4 4l16 16\\"/>'),
  "VIEW": SVG('<path d=\\"M7 17L17 7M10 7h7v7\\"/>'),
}
patch('"SHARE": "<svg class=\\"ri ri-arrow\\"', ''.join('"%s": "%s", ' % kv for kv in ICONS.items()) + '"SHARE": "<svg class=\\"ri ri-arrow\\"', 'new icons')
ICO = lambda k: "(0,L.jsx)(`span`,{className:`pp-ic mt-ic`,dangerouslySetInnerHTML:{__html:_ppIco(" + k + ")}})"

# turn a (0,L.jsx)(`button`|`a`,{... STYLE ,children:`LABEL`}) into a pill with an icon
def pill(old_tail, cls, icon, label, n=1, tag="`button`"):
    global c
    for _ in range(n):
        i = c.index(old_tail); j = c.rindex("(0,L.jsx)(" + tag, 0, i)
        c = c[:j] + "(0,L.jsxs)" + c[j + len("(0,L.jsx)"):i] + "className:" + cls + ",children:[" + ICO(icon) + "," + label + "]}" + c[i + len(old_tail):]
    print('OK: pill', label, n)

# post mod tools: label and Delete
patch("children:[`🛡️ Mod tools `,", "children:[" + ICO("`SHIELD`") + ",`Mod tools `,", 'shield label')
pill("children:`🗑️ Delete`}", "`mod-tool danger`", "`TRASH`", "`Delete`")

# mod panel: Deleted and Archived lists
V = "style:{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#1e3a5f`,color:`#60a5fa`,fontWeight:600,fontSize:12,cursor:`pointer`,textDecoration:`none`,display:`inline-block`},children:`View`}"
if c.count(V) != 2: print('FAIL view', c.count(V)); sys.exit(1)
pill(V, "`mod-tool mp`", "`VIEW`", "`View`", 2, tag="`a`")
pill("style:{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#14532d`,color:`#4ade80`,fontWeight:600,fontSize:12,cursor:`pointer`},children:`Restore`}", "`mod-tool mp`", "`RESTORE`", "`Restore`")
pill("style:{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#14532d`,color:`#4ade80`,fontWeight:600,fontSize:12,cursor:`pointer`},children:`Unarchive`}", "`mod-tool mp`", "`ARCHIVE`", "`Unarchive`")
D = "style:{padding:`6px 12px`,borderRadius:8,border:`none`,background:`#450a0a`,color:`#f87171`,fontWeight:600,fontSize:12,cursor:`pointer`},children:`Delete`}"
if c.count(D) != 2: print('FAIL delete', c.count(D)); sys.exit(1)
pill(D, "`mod-tool danger mp`", "`TRASH`", "`Delete`", 2)
pill("style:{padding:`4px 10px`,borderRadius:8,border:`none`,background:`#450a0a`,color:`#f87171`,fontWeight:600,fontSize:12,cursor:`pointer`},children:`Delete All`}", "`mod-tool danger mp`", "`TRASH`", "`Delete All`")
pill("style:{padding:`6px 12px`,borderRadius:8,border:`1px solid #374151`,background:e.archived?`#3b2a52`:`transparent`,color:e.archived?`#c084fc`:`#94a3b8`,fontWeight:600,fontSize:12,cursor:`pointer`},children:e.archived?`Show to members`:`Hide from members`}",
     "`mod-tool mp`+(e.archived?` on`:``)", "e.archived?`EYE`:`EYEOFF`", "e.archived?`Show to members`:`Hide from members`")

# purple everywhere (orange before); Delete stays red. `body` raises specificity over the original rules.
css = ("body .mod-tools{border-top-color:rgba(192,132,252,.22)}"
       "body .mod-tools-label{color:#c084fc;display:inline-flex;align-items:center}"
       "body .mod-tools-label .mt-ic{margin:0 5px 0 0}body .mod-tools-label .mt-ic .ri{width:13px;height:13px;stroke-width:2.4;display:block}"
       "body .mod-tool{border-color:rgba(192,132,252,.45);background:rgba(192,132,252,.08);color:#c084fc}"
       "body .mod-tool.on{background:#c084fc;border-color:#c084fc;color:#14081d}"
       "body .mod-tool.danger{border-color:rgba(248,113,113,.45);background:rgba(248,113,113,.08);color:#f87171}"
       "body .mod-tool.mp{height:30px;padding:0 12px;font-size:12px;text-decoration:none;font-family:inherit;box-sizing:border-box}"
       "body .post-badge:not(.bot){border-color:rgba(192,132,252,.45);background:rgba(192,132,252,.08)}"
       "body .post-badge.pp-badge-ic{color:#c084fc}")
patch(".mod-tool .mt-ic{margin:0 5px 0 -2px}", css + ".mod-tool .mt-ic{margin:0 5px 0 -2px}", 'purple styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
