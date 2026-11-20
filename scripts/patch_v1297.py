#!/usr/bin/env python3
"""Patch v1296 -> v1297: Share sheet fixes.
- Keyboard open: the overlay follows the visual viewport (iOS), so the sheet sits right on the keyboard and the page
  doesn't show between them.
- Huddle circles: two birds bigger, overlapping in the middle, facing each other (like the approved preview).
- In the post scroller the sheet is black (matches the scroller; no dark strip under it)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1296.js'
dst = '_deploy/assets/index-DUcNPOLc-v1297.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("body .ps-b1{left:3px;top:4px}body .ps-b2{right:2px;bottom:3px;transform:scaleX(-1)}",
      "body .ps-b1{left:5px;top:7px;z-index:1}body .ps-b2{right:4px;bottom:6px;transform:scaleX(-1)}", 'bird positions')
patch("children:_ppFace(o[0],23)},`a`),(0,L.jsx)(`span`,{className:`ps-b ps-b2`,children:_ppFace(o[1],23)}",
      "children:_ppFace(o[0],26)},`a`),(0,L.jsx)(`span`,{className:`ps-b ps-b2`,children:_ppFace(o[1],26)}", 'bird size')
patch("children:_ppFace(o[0],32)}", "children:_ppFace(o[0],34)}", 'solo size')
patch("body .ps-note{", "html.reel-shown .ps-sheet{background:#000;border:1px solid #2a2d36;border-bottom:0}html.reel-shown .ps-ov{background:rgba(0,0,0,.6)}body .ps-note{", 'black in scroller')
# follow the visual viewport while the sheet is open (keyboard)
patch("const bye=()=>{setIn(!1);setTimeout(close,240)};",
      "const ovR=(0,_.useRef)(null);(0,_.useEffect)(()=>{const vv=window.visualViewport;if(!vv)return;const fit=()=>{const o=ovR.current;if(!o)return;o.style.top=vv.offsetTop+`px`;o.style.height=vv.height+`px`;o.style.bottom=`auto`};fit();vv.addEventListener(`resize`,fit);vv.addEventListener(`scroll`,fit);return()=>{vv.removeEventListener(`resize`,fit);vv.removeEventListener(`scroll`,fit)}},[]);"
      "const bye=()=>{setIn(!1);setTimeout(close,240)};", 'visual viewport')
patch("return(0,L.jsx)(`div`,{className:`ps-ov`+(inn?` in`:``),onClick:bye,children:", "return(0,L.jsx)(`div`,{ref:ovR,className:`ps-ov`+(inn?` in`:``),onClick:bye,children:", 'ref')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
