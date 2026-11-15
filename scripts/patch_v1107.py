#!/usr/bin/env python3
"""Patch v1106 -> v1107: the Flock page controls match the other mod controls: purple pills with line icons
(Cage, Ban, Ban IP, Make Mod / Demote, Make Admin, Delete, Bring back, Delete forever), and the account-lock badge
uses the drawn padlock instead of the emoji. Dangerous ones (Ban, Ban IP, Delete) are red."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1106.js'
dst = '_deploy/assets/index-DUcNPOLc-v1107.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
SVG = lambda body: ('<svg class=\\"ri\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" '
                    'stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">' + body + '</svg>')
ICONS = {
  "CAGE": SVG('<path d=\\"M12 2.5V4.5\\"/><path d=\\"M6 20.5V11a6 6 0 0 1 12 0v9.5\\"/><path d=\\"M4 20.5h16\\"/><path d=\\"M10 5.3v15.2M14 5.3v15.2\\"/>'),
  "BAN": SVG('<circle cx=\\"12\\" cy=\\"12\\" r=\\"8.5\\"/><path d=\\"M6 6l12 12\\"/>'),
  "GLOBE": SVG('<circle cx=\\"12\\" cy=\\"12\\" r=\\"8.5\\"/><path d=\\"M3.5 12h17\\"/><path d=\\"M12 3.5c2.4 2.4 3.6 5.2 3.6 8.5s-1.2 6.1-3.6 8.5c-2.4-2.4-3.6-5.2-3.6-8.5S9.6 5.9 12 3.5z\\"/>'),
  "UP": SVG('<path d=\\"M12 19V5\\"/><path d=\\"M6 11l6-6 6 6\\"/>'),
  "DOWN": SVG('<path d=\\"M12 5v14\\"/><path d=\\"M6 13l6 6 6-6\\"/>'),
}
patch('"SHARE": "<svg class=\\"ri ri-arrow\\"', ''.join('"%s": "%s", ' % kv for kv in ICONS.items()) + '"SHARE": "<svg class=\\"ri ri-arrow\\"', 'new icons')
ICO = lambda k: "(0,L.jsx)(`span`,{className:`pp-ic mt-ic`,dangerouslySetInnerHTML:{__html:_ppIco(" + k + ")}})"
def pill(old_tail, cls, icon, label):
    global c
    if c.count(old_tail) != 1: print('FAIL', label, c.count(old_tail)); sys.exit(1)
    i = c.index(old_tail); j = c.rindex("(0,L.jsx)(`button`", 0, i)
    c = c[:j] + "(0,L.jsxs)" + c[j + len("(0,L.jsx)"):i] + "className:" + cls + ",children:[" + ICO(icon) + "," + label + "]}" + c[i + len(old_tail):]
    print('OK: pill', label)

pill("style:{padding:`2px 8px`,borderRadius:6,border:`none`,background:c?`#78350f`:`#451a03`,color:c?`#fde68a`:`#fbbf24`,fontWeight:600,cursor:`pointer`,fontSize:10},children:c?`Uncage`:`🪹 Cage`}",
     "`mod-tool fs`+(c?` on`:``)", "`CAGE`", "c?`Uncage`:`Cage`")
pill("style:{padding:`2px 8px`,borderRadius:6,border:`none`,background:s?`#1f2937`:`#7f1d1d`,color:s?`#f8fafc`:`#fca5a5`,fontWeight:600,cursor:`pointer`,fontSize:10},children:s?`Unban`:`Ban`}",
     "s?`mod-tool fs`:`mod-tool danger fs`", "`BAN`", "s?`Unban`:`Ban`")
pill("style:{padding:`2px 8px`,borderRadius:6,border:`1px solid #7f1d1d`,background:`transparent`,color:`#fca5a5`,fontWeight:600,cursor:`pointer`,fontSize:10},children:`🌐 Ban IP`}",
     "`mod-tool danger fs`", "`GLOBE`", "`Ban IP`")
pill("style:{padding:`2px 8px`,borderRadius:6,border:`none`,background:f?`#1f2937`:`#c084fc`,color:f?`#f8fafc`:`#14081d`,fontWeight:600,fontSize:10,cursor:`pointer`},children:d?`→ Mod`:u?`Demote`:`→ Mod`}",
     "`mod-tool fs`", "f?`DOWN`:`UP`", "d?`Make Mod`:u?`Demote`:`Make Mod`")
pill("style:{padding:`2px 8px`,borderRadius:6,border:`none`,background:`#fb923c`,color:`#14081d`,fontWeight:600,fontSize:10,cursor:`pointer`},children:`→ Admin`}",
     "`mod-tool fs`", "`UP`", "`Make Admin`")
pill("style:{padding:`2px 8px`,borderRadius:6,border:`1px solid #374151`,background:`transparent`,color:`#f87171`,fontWeight:600,fontSize:10,cursor:`pointer`},children:`Delete`}",
     "`mod-tool danger fs`", "`TRASH`", "`Delete`")
pill("style:{padding:`4px 10px`,borderRadius:6,border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:11,cursor:`pointer`,whiteSpace:`nowrap`},children:`Bring back`}",
     "`mod-tool fs`", "`RESTORE`", "`Bring back`")
pill("style:{padding:`4px 10px`,borderRadius:6,border:`1px solid #374151`,background:`transparent`,color:`#f87171`,fontWeight:600,fontSize:11,cursor:`pointer`,whiteSpace:`nowrap`},children:`Delete forever`}",
     "`mod-tool danger fs`", "`TRASH`", "`Delete forever`")
# account-lock badge: drawn padlock instead of the emoji
patch("children:[`🔒 Locked · ${left}m`,", "children:[(0,L.jsx)(`span`,{className:`pp-ic lk-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`LOCK`)}}),`Locked · ${left}m`,", 'lock badge')
css = ("body .mod-tool.fs{height:26px;padding:0 10px;font-size:11px;font-family:inherit;box-sizing:border-box}"
       "body .mod-tool.fs .mt-ic .ri{width:12px;height:12px}"
       "body .lk-badge .lk-ic{margin:0 -2px 0 -1px}body .lk-badge .lk-ic .ri{width:11px;height:11px;stroke-width:2.5;display:block}")
patch("body .mod-tool.mp{", css + "body .mod-tool.mp{", 'flock pill styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
