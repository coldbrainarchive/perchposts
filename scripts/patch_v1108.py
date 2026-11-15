#!/usr/bin/env python3
"""Patch v1107 -> v1108: no emoji as system symbols in chirps.
- Section labels (Pinned / Latest / Top / Most replied / Highlights / Media), the chirp filter button and its menu, and the
  "+N more pinned" note use line icons (same style as flap / chirp / share) in place of the emoji.
- The pin on pinned chirps is our pin icon in black.
- Huddle system lines (joined / left / back / added / removed / declined / now runs the huddle) show a line icon instead of
  the emoji the server stores; the text-matching that jumps to them ignores that icon."""
import sys, urllib.parse
src = '_deploy/assets/index-DUcNPOLc-v1107.js'
dst = '_deploy/assets/index-DUcNPOLc-v1108.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
BODY = {
  "CLOCK": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
  "FLAME": '<path d="M12 21c3.6 0 6.3-2.5 6.3-6.1 0-3.3-2.1-5.7-4-7.8-.2 1.9-1.2 3.2-2.4 3.7.2-3-1-5.8-3.2-7.3.1 3-1.8 5-3.3 6.9-1 1.3-1.7 2.7-1.7 4.5C5.7 18.5 8.4 21 12 21z"/>',
  "REPLY": '<path d="M9 14.5l-5-5 5-5"/><path d="M4 9.5h10.5a5.5 5.5 0 0 1 0 11H12"/>',
  "SPARK": '<path d="M11 3.5l1.9 5.1 5.1 1.9-5.1 1.9L11 17.5l-1.9-5.1L4 10.5l5.1-1.9z"/><path d="M18.5 15v5M16 17.5h5"/>',
  "IMAGE": '<rect x="3" y="4.5" width="18" height="15" rx="2.5"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="M21 15.5l-5-5-9.5 9"/>',
  "JOIN": '<circle cx="9.5" cy="8" r="3.5"/><path d="M3.5 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M19 8v6M16 11h6"/>',
  "LEAVE": '<path d="M14 4h3.5A2.5 2.5 0 0 1 20 6.5v11a2.5 2.5 0 0 1-2.5 2.5H14"/><path d="M9 16l-4-4 4-4"/><path d="M5 12h10"/>',
  "CROWN": '<path d="M4.5 17L3.5 8l4.8 3.6L12 6l3.7 5.6L20.5 8l-1 9z"/><path d="M5 20.5h14"/>',
  "REMOVE": '<circle cx="9.5" cy="8" r="3.5"/><path d="M3.5 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 11h6"/>',
}
esc = lambda s: s.replace('"', '\\"')
SVG = lambda b: esc('<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + b + '</svg>')
patch('"SHARE": "<svg class=\\"ri ri-arrow\\"', ''.join('"%s": "%s", ' % (k, SVG(b)) for k, b in BODY.items()) + '"SHARE": "<svg class=\\"ri ri-arrow\\"', 'new icons')

# helpers: split a leading emoji off a label, and turn it into our icon
helpers = (
  "const _PPE={\"📌\":`PIN`,\"🕒\":`CLOCK`,\"🔥\":`FLAME`,\"↩️\":`REPLY`,\"↩\":`REPLY`,\"✨\":`SPARK`,\"🖼️\":`IMAGE`,\"🖼\":`IMAGE`};\n"
  "function _ppSplit(s){s=String(s||``);const m=s.match(/^(\\p{Extended_Pictographic}\\uFE0F?)\\s*/u);return m?[m[1],s.slice(m[0].length)]:[null,s]}\n"
  "function _ppLbl(s){const[e,t]=_ppSplit(s),k=e&&_PPE[e];return k?[(0,L.jsx)(`span`,{className:`pp-ic lb-ic`,dangerouslySetInnerHTML:{__html:_ppIco(k)}},`i`),t]:s}\n"
  "function _ppSysK(s){const[e,t]=_ppSplit(s);if(!e)return null;return e===`👑`?`CROWN`:e===`🚫`?`BAN`:e===`💨`?`REMOVE`:/ left /.test(` `+t+` `)?`LEAVE`:`JOIN`}\n"
  "function _ppSysLbl(s){const k=_ppSysK(s),t=_ppSplit(s)[1];return k?[(0,L.jsx)(`span`,{className:`pp-ic lb-ic`,dangerouslySetInnerHTML:{__html:_ppIco(k)}},`i`),t]:t}\n")
patch("function _ppFlapAnim(root){", helpers + "function _ppFlapAnim(root){", 'label helpers')

# section labels, filter button + menu, more-pinned note
patch("(0,L.jsx)(`span`,{className:`chat-section-pill`,children:_x})", "(0,L.jsx)(`span`,{className:`chat-section-pill`,children:_ppLbl(_x)})", 'section labels')
patch("\"aria-label\":`Chirp preview: ${_CPL[_cpm]}`", "\"aria-label\":`Chirp preview: ${_ppSplit(_CPL[_cpm])[1]}`", 'filter label text')
patch("children:[_CPL[_cpm].replace(` chirps`,``),(0,L.jsx)(`span`,{className:`cp-caret`", "children:[...[].concat(_ppLbl(_CPL[_cpm].replace(` chirps`,``))),(0,L.jsx)(`span`,{className:`cp-caret`", 'filter button')
patch("b.className=`cp-opt`+(k===cur?` on`:``);b.textContent=lb;",
      "b.className=`cp-opt`+(k===cur?` on`:``);{const[_e,_t]=_ppSplit(lb),_k=_e&&_PPE[_e];if(_k)b.innerHTML=`<span class=\"pp-ic lb-ic\">`+_ppIco(_k)+`</span>`;b.append(_t)}", 'filter menu')
patch("children:`📌 +${_pmo} more pinned`", "children:_ppLbl(`📌 +${_pmo} more pinned`)", 'more pinned note')

# the pin on pinned chirps: our pin, black
patch("e.pinned&&(0,L.jsx)(`span`,{style:{fontSize:11,color:`#c084fc`,flexShrink:0},children:`📌`})",
      "e.pinned&&(0,L.jsx)(`span`,{className:`pp-ic pin-mk`,title:`Pinned`,style:{color:`#0a0a0a`,flexShrink:0},dangerouslySetInnerHTML:{__html:_ppIco(`PIN`)}})", 'pinned chirp pin')

# huddle system lines: icon via CSS (data-ic), text without the emoji (so the jump-to code's text match still works)
patch("className:`chat-sys`,style:{textAlign:`center`,color:`#64748b`,fontSize:12,padding:`5px 12px`,fontStyle:`italic`,userSelect:`none`},children:e.content})",
      "className:`chat-sys`,\"data-ic\":_ppSysK(e.content)||void 0,style:{textAlign:`center`,color:`#64748b`,fontSize:12,padding:`5px 12px`,fontStyle:`italic`,userSelect:`none`},children:_ppSplit(e.content)[1]})", 'system lines')
for v, n in [('_sc', 2), ('_ac', 1), ('_cr', 1)]:
    patch("(_d.textContent||``).trim()===(" + v + ".content||``).trim()", "(_d.textContent||``).trim()===_ppSplit(" + v + ".content)[1].trim()", 'jump match ' + v, n)
patch("sys?null:`: `,_hxText(last.c)]", "sys?null:`: `,sys?_ppSysLbl(last.c):_hxText(last.c)]", 'huddle list preview')

# styles: label icons, the black pin, and the system-line icons as masks
def mask(k):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + (BODY.get(k) or '<circle cx="12" cy="12" r="8.5"/><path d="M6 6l12 12"/>') + '</svg>'
    return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe=' /:=,.-') + '")'
sysc = ''.join('.chat-sys[data-ic=%s]{--ppic:%s}' % (k, mask(k)) for k in ['JOIN', 'LEAVE', 'CROWN', 'REMOVE', 'BAN'])
css = ("body .lb-ic{display:inline-flex;vertical-align:-.16em;margin-right:.4em}body .lb-ic .ri{width:1.15em;height:1.15em;stroke-width:2.2;display:block}"
       "body .cp-opt .lb-ic{margin-right:.55em}body .pin-mk .ri{width:13px;height:13px;stroke-width:2.4;display:block}"
       ".chat-sys[data-ic]::before{content:\\\"\\\";display:inline-block;width:13px;height:13px;margin:0 6px -2px 0;background:currentColor;-webkit-mask:var(--ppic) center/contain no-repeat;mask:var(--ppic) center/contain no-repeat}"
       + sysc)
patch("body .mod-tool.fs{", css + "body .mod-tool.fs{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
