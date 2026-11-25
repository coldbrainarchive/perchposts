#!/usr/bin/env python3
"""Patch v1390 -> v1391: the huddle members list closes when you tap its "Members" heading or the chat area below
it (same shrink animation as the grab bar). "+ Invite" / Cancel and the message bar keep working."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1390.js'
dst = '_deploy/assets/index-DUcNPOLc-v1391.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

# panel: expose the animated close, and a see-through catcher over the chat below (huddles)
patch("function _ChXP({close,slot,dock}){const R0=(0,_.useRef)(null),[bye,setBye]=(0,_.useState)(!1),dg=(0,_.useRef)(null);\n const shut=()=>{if(bye)return;setBye(!0);setTimeout(close,190)};",
      "function _ChXP({close,slot,dock}){const R0=(0,_.useRef)(null),BD=(0,_.useRef)(null),[bye,setBye]=(0,_.useState)(!1),dg=(0,_.useRef)(null);\n const shut=()=>{if(bye)return;setBye(!0);setTimeout(close,190)};window._chxShut=shut;(0,_.useEffect)(()=>()=>{window._chxShut=null},[]);", 'expose shut')
patch("el.style.maxHeight=(par.clientHeight-(cm?cm.offsetHeight:0))+`px`};",
      "el.style.maxHeight=(par.clientHeight-(cm?cm.offsetHeight:0))+`px`;if(BD.current)BD.current.style.bottom=(cm?cm.offsetHeight:0)+`px`};", 'catcher stops above message bar')
i = c.index("function _ChXP({close,slot,dock}){"); j = c.index("\nfunction ", i + 10)
body = c[i:j]
old_ret = "return(0,L.jsxs)(`div`,{ref:R0,className:`ch-xp`"
body = body.rstrip("\n"); assert body.count(old_ret) == 1 and body.endswith("]})}")
body = body.replace(old_ret, "return(0,L.jsxs)(L.Fragment,{children:[dock.post.is_huddle?(0,L.jsx)(`div`,{ref:BD,className:`ch-xp-bd`,onClick:ev=>{ev.stopPropagation();shut()}},`bd`):null,(0,L.jsxs)(`div`,{ref:R0,className:`ch-xp`")
body = body[:-len("]})}")] + "]},`xp`)]})}"
c = c[:i] + body + "\n" + c[j:]
print('OK catcher + fragment')

# the "Members" heading closes the inline list
patch("(0,L.jsxs)(`div`,{className:`hx-sh`,children:[inv?`Invite birds`:`Members`",
      "(0,L.jsxs)(`div`,{className:`hx-sh`,onClick:inline?()=>{window._chxShut?window._chxShut():close()}:void 0,style:inline?{cursor:`pointer`}:void 0,children:[inv?`Invite birds`:`Members`", 'heading closes')

patch("body .lb-ic{", "body .ch-xp-bd{position:absolute;left:0;right:0;top:0;z-index:29;background:transparent;-webkit-tap-highlight-color:transparent}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
